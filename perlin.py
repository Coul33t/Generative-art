import numpy as np

def generate_perlin_noise_2d(shape, res):
    def f(t):
        return 6 * t**5 - 15 * t**4 + 10 * t**3

    delta = (res[0] / shape[0], res[1] / shape[1])
    d = (shape[0] // res[0], shape[1] // res[1])
    grid = np.mgrid[0:res[0]:delta[0], 0:res[1]:delta[1]].transpose(1, 2, 0) % 1
    # Gradients
    angles = 2 * np.pi * np.random.rand(res[0] + 1, res[1] + 1)
    gradients = np.dstack((np.cos(angles), np.sin(angles)))
    g00 = gradients[0: -1, 0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g10 = gradients[1:, 0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g01 = gradients[0: -1, 1:].repeat(d[0], 0).repeat(d[1], 1)
    g11 = gradients[1:, 1:].repeat(d[0], 0).repeat(d[1], 1)
    # Ramps
    n00 = np.sum(grid * g00, 2)
    n10 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1])) * g10, 2)
    n01 = np.sum(np.dstack((grid[:, :, 0], grid[:, :, 1] - 1)) * g01, 2)
    n11 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1] - 1)) * g11, 2)
    # Interpolation
    t = f(grid)
    n0 = n00 * (1 - t[:, :, 0]) + t[:, :, 0] * n10
    n1 = n01 * (1 - t[:, :, 0]) + t[:, :, 0] * n11
    return np.sqrt(2) * ((1 - t[:, :, 1]) * n0 + t[:, :, 1] * n1)

def generate_fractal_noise_2d(shape, res, octaves=1, persistence=0.5):
    noise = np.zeros(shape)
    frequency = 1
    amplitude = 1

    for _ in range(octaves):
        noise += amplitude * generate_perlin_noise_2d(shape, (frequency * res[0], frequency * res[1]))
        frequency *= 2
        amplitude *= persistence

    return noise

def test():

    from PIL import Image

    img_array = []

    img_size = (256, 256)


    for i in range(1, 5):
        print(f'res : ({2**i}, {2**i})')
        for j in range(1, 5):
            print(f'octaves : {j}')
            img = generate_fractal_noise_2d(img_size, (2**i, 2**i), octaves=j, persistence=0.5)
            img = img + abs(np.amin(img))
            img = img / np.amax(img)
            img *= 255
            #img = Image.fromarray(img.astype('uint8').T, 'L')
            img_array.append(img)


    final_img = np.ndarray((0, 0))
    tmp_imgs = []

    for i in range(4):
        tmp_imgs.append(np.concatenate(img_array[i*4: (i*4) + 4]))

    final_img = np.concatenate(tmp_imgs, axis=1)
    final_img = Image.fromarray(final_img.astype('uint8').T, 'L')
    final_img.show()

if __name__ == '__main__':
    test()
