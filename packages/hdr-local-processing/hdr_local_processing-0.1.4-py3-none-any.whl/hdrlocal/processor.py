import glob
import cv2
import numpy
import os

import util
import clahe


class LocalProcessor:
    def __init__(self):
        # -------------------------------
        self.root = "./test_images/"
        self.ext = "*.bmp"
        # -------------------------------

    # -------------------------------
    # File load methods
    # -------------------------------
    def open_image(self, item):
        print(f"item {item}")
        img = cv2.imread(item)
        try:
            return cv2.cvtColor(img, code=cv2.COLOR_BGR2RGB)
        except Exception as e:
            print(e)


    def load_images(self, root, folder, ext=None):
        ext = self.ext if ext is None else ext

        glob_path = os.path.join(root, folder, ext)
        iter_items = glob.iglob(glob_path)
        images = []
        exposures = []
        for item in iter_items:
            img = self.open_image(item)
            images.append(img)
            fname = os.path.basename(item)
            num = int(fname[:-4].split('_')[-1])
            den = 1000
            exposures.append(int(num / den))
        iter_tuple = zip(images, exposures)
        sorted_iter_tuple = sorted(iter_tuple, key=lambda pair: pair[1], reverse=True)
        sorted_images = [img for img, times in sorted_iter_tuple]
        # TODO Check if ascended or descended exposure affect result.
        # TODO Check if devision by 1000 affect result
        sorted_exposures = sorted(exposures, reverse=True)
        sorted_log_exposures = numpy.log(sorted_exposures)

        return [sorted_images, sorted_log_exposures]

    def root_iterate(self, root=None):
        root = self.root if root is None else root
        processing_list = []
        for foldername in os.listdir(root):
            print(foldername)
            processing_list.append(self.load_images(root, foldername))
        print(len(processing_list))
        return processing_list

    # -------------------------------
    # Processing method
    # -------------------------------
    
    def run_local(self, images, exposures, lambda_=50, num_px=150, gamma=1.0, saturation=2.5, numtiles=24):
        log_exposures = numpy.log(exposures)

        crf_channel, _, w = self.hdr_debevec(images, log_exposures, lambda_=lambda_, num_px=num_px)

        irradiance_map = self.compute_irradiance(crf_channel, w, images, log_exposures)

        result_bgr = self.local_tonemap(irradiance_map,  gamma_=gamma, saturation=saturation, numtiles=(numtiles, numtiles))

        result = result_bgr[:, :, [2, 1, 0]]

        return result

    def hdr_debevec(self, images, exposures, lambda_=50, num_px=150):
        num_images = len(images)
        Zmin = 0
        Zmax = 255

        # image parameters
        H, W, C = images[0].shape

        # optmization parameters
        px_idx = numpy.random.choice(H * W, (num_px,), replace=False)

        # define pixel intensity weighting function w
        w = numpy.concatenate((numpy.arange(128) - Zmin, Zmax - numpy.arange(128, 256)))

        # compute Z matrix
        Z = numpy.empty((num_px, num_images))
        crf_channel = []
        log_irrad_channel = []
        for ch in range(C):
            for j, image in enumerate(images):
                flat_image = image[:, :, ch].flatten()
                Z[:, j] = flat_image[px_idx]

            # get crf and irradiance for each color channel
            [crf, log_irrad] = self.crf_solve(Z.astype('int32'), exposures, lambda_, w, Zmin, Zmax)
            crf_channel.append(crf)
            log_irrad_channel.append(log_irrad)

        return [crf_channel, log_irrad_channel, w]

    def crf_solve(self, Z, B, lambda_, w, Zmin, Zmax):
        n = Zmax + 1
        num_px, num_im = Z.shape
        A = numpy.zeros((num_px * num_im + n, n + num_px))
        b = numpy.zeros((A.shape[0]))

        # include the data fitting equations
        k = 0
        for i in range(num_px):
            for j in range(num_im):
                wij = w[Z[i, j]]
                A[k, Z[i, j]] = wij
                A[k, n + i] = -wij
                b[k] = wij * B[j]
                k += 1

        # fix the curve by setting its middle value to 0
        A[k, n // 2] = 1
        k += 1

        # include the smoothness equations
        for i in range(n - 2):
            A[k, i] = lambda_ * w[i + 1]
            A[k, i + 1] = -2 * lambda_ * w[i + 1]
            A[k, i + 2] = lambda_ * w[i + 1]
            k += 1

        # solve the system using LLS
        output = numpy.linalg.lstsq(A, b)
        x = output[0]
        g = x[:n]
        lE = x[n:]
        del A, b
        return [g, lE]

    def compute_irradiance(self, crf_channel, w, images, exposures):
        H, W, C = images[0].shape
        num_images = len(images)

        # irradiance map for each color channel
        irradiance_map = numpy.empty((H * W, C))
        for ch in range(C):
            crf = crf_channel[ch]
            num_ = numpy.empty((num_images, H * W))
            den_ = numpy.empty((num_images, H * W))
            for j in range(num_images):
                flat_image = (images[j][:, :, ch].flatten()).astype('int32')
                num_[j, :] = numpy.multiply(w[flat_image], crf[flat_image] - exposures[j])
                den_[j, :] = w[flat_image]

            irradiance_map[:, ch] = numpy.sum(num_, axis=0) / (numpy.sum(den_, axis=0) + 1e-6)

        irradiance_map = numpy.reshape(numpy.exp(irradiance_map), (H, W, C))

        return irradiance_map

    def local_tonemap(self, E, l_remap=(0, 1), gamma_=1.0, saturation=2.5, numtiles=(24, 24)):
        """
            render HDR for viewing
            exposure estimate -> log2 -> CLAHE -> remap to l_remap -> gamma correction -> HDR
            @param E: exposure (N x M x 3)
            @param l_remap: remap intensity to l_remap in the image adjust step
            @param saturation: saturation of the color.
            @param numtiles: number of contextual tiles in the CLAHE step
            return contrast reduced image
        """
        if E.shape[0] % numtiles[0] != 0 or E.shape[1] % numtiles[1] != 0:
            E = util.crop_image(E, (E.shape[0] // numtiles[0] * numtiles[0], E.shape[1] // numtiles[1] * numtiles[1]))
        l2E, has_nonzero = self.lognormal(E)
        if has_nonzero:
            I = self.tone_operator(l2E, l_remap, saturation, gamma_, numtiles)
        else:
            I = l2E
        # clip
        I[I < 0] = 0
        I[1 < I] = 1
        del E
        return numpy.uint8(I * 255.)

    def lognormal(self, E):
        """
            log2(E). remove 0s.
            return log2E, has_nonzero
        """
        mask = (E != 0)

        if numpy.any(mask):
            min_nonzero = numpy.min(E[mask])
            E[numpy.logical_not(mask)] = min_nonzero
            l2E = util.rescale(numpy.log2(E))
            has_nonzero = True

        else:  # all elements are zero
            l2E = numpy.zeros_like(E)
            has_nonzero = False

        return l2E, has_nonzero

    def tone_operator(self, l2E, l_remap, saturation, gamma_, numtiles):
        """
            The main algorithm is CLAHE: contrast limited adaptive histogram equalization
            preprocessing: convert RGB to XYZ to Lab
            postprocessing: back to RGB
        """
        lab = util.srgb2lab(l2E)
        lab[:, :, 0] = util.rescale(lab[:, :, 0])
        #    lab[:, :, 0] /= 100
        lab[:, :, 0] = clahe.hist_equalize(lab[:, :, 0], numtiles)
        lab[:, :, 0] = self.imadjust(lab[:, :, 0], range_in=l_remap, range_out=(0, 1), gamma=gamma_) * 100
        lab[:, :, 1:] = lab[:, :, 1:] * saturation
        I = util.lab2srgb(lab)
        return I

    def imadjust(self, I, range_in=None, range_out=(0, 1), gamma=1):
        """
            remap I from range_in to range_out
            @param I: image
            @param range_in: range of the inumpyut image. will be assigned minmax(I) if none
            @param range_out: range of the output image
            @param gamma: factor of the gamma correction
        """
        if range_in is None:
            range_in = (numpy.min(I), numpy.max(I))
        out = (I - range_in[0]) / (range_in[1] - range_in[0])
        out = out ** gamma
        out = out * (range_out[1] - range_out[0]) + range_out[0]
        return out
        
    
if __name__ == "__main__":
    processing_list = LocalProcessor().root_iterate()
    result_list = []
    for bunch in processing_list:
        image, exposures = bunch
        result_list.append(LocalProcessor().run_local(image, exposures))

    for idx, im in enumerate(result_list):
        print(im.shape)
        cv2.imwrite(f"./{idx}.png", im)
