from augraphy import *
import os
import random
import cv2


################################################################################
# CONTROLLING VARIATION
#
# We can control the outputs of the pipeline by setting values here.
################################################################################

# Dithering.dither_type can be 'ordered' for ordered dithering or another string for floyd-steinberg dithering
dithering_dither_type = random.choice(["ordered", "floyd-steinberg"])
# Dithering.order determines the dimensions of the threshold map
dithering_order = random.choice(range(1,10))

# InkBleed.intensity_range is a tuple with bounds for bleed intensity to be selected from
inkbleed_intensity_range = (0.1, 0.2)
# InkBleed.color_range is a tuple with bounds for color noise
inkbleed_color_range = (0, 224)
# InkBleed.kernel_size determines the radius of the bleed effect
inkbleed_kernel_size = (5, 5)
# InkBleed.severity determines significance of bleed effect
inkbleed_severity=(0.4, 0.6)

# BleedThrough.intensity_range is a tuple with bounds for bleed intensity to be selected from
bleedthrough_intensity_range=(0.1, 0.2)
# BleedThrough.color_range is a tuple with bounds for color noise
bleedthrough_color_range=(0, 224)
# BleedThrough.ksize is a tuple of height/width pairs for sampling kernel size
bleedthrough_ksize=(17, 17)
# BleedThrough.sigmaX is the standard deviation of the kernel along the x-axis
bleedthrough_sigmaX=0
# BleedThrough.alpha is the intensity of the bleeding effect, recommended 0.1-0.5
bleedthrough_alpha=0.3
# BleedThrough.offsets is a pair of x and y distances to shift the bleed with
bleedthrough_offsets=(10, 20)

# Letterpress.n_samples is a tuple determining how many points to generate per cluster
letterpress_n_samples=(100, 200)
# Letterpress.n_clusters is a tuple determining how many clusters to generate
letterpress_n_clusters=(500, 1000)
# Letterpress.std_range is a pair of ints determining the std deviation range in each blob
letterpress_std_range=(500, 500)
# Letterpress.value_range determines values that points in the blob are sampled from
letterpress_value_range=(200, 255)
# Letterpress.value_threshold_range is the minimum pixel value to enable the effect (e.g. 128)
letterpress_value_threshold_range=(128, 128)
# Letterpress.blur enables blur in the noise mask
letterpress_blur=1

# LowInkLines.count_range is a pair determining how many lines should be drawn
lowinkrandomlines_count_range = (5, 10)
lowinkperiodiclines_count_range = (2, 5)
# LowInkLines.use_consistent_lines is false if we should vary the width and alpha of lines
lowinkrandomlines_use_consistent_lines=random.choice([True, False])
lowinkperiodiclines_use_consistent_lines=random.choice([True, False])
# LowInkPeriodicLines.period_range is a pair determining how wide the gap between lines can be
lowinkperiodiclines_period_range=(10, 30)

# PaperFactory.tile_texture_shape determines the range from which to sample texture dimensions
paperfactory_tile_texture_shape = (250, 250)
# PaperFactory.texture_path is the directory to pull textures from
paperfactory_texture_path = "./paper_textures"

# NoiseTexturize.sigma_range defines bounds of noise fluctuations
noisetexturize_sigma_range = (3, 10)
# NoiseTexturize.turbulence_range defines how quickly big patterns are replaced with small ones; lower means more iterations
noisetexturize_turbulence_range = (2, 5)

# BrightnessTexturize.range determines the value range of samples for the brightness matrix
brightnesstexturize_range = (0.9, 0.99)
# BrightnessTexturize.deviation is additional variation for the uniform sample
brightnesstexturize_deviation = 0.03

# Brightness.range is a pair of floats determining the brightness delta
brightness_range = (0.8, 1.4)

# PageBorder.side determines the page edge of the effect
pageborder_side = random.choice(["left", "top", "bottom", "right"])
# PageBorder.width_range determines border thickness
pageborder_width_range = (5, 30)
# PageBorder.pages determines how many page shadows to render
pageborder_pages = None # internally this is random.randint(2, 7)

# DirtyRollers.line_width_range determines the width of roller lines
dirtyrollers_line_width_range = (8, 12)
# DirtyRollers.scanline_type changes the background of lines
dirtyrollers_scanline_type = 0

# LightingGradient.mask_size determines how big the mask should be
lightinggradient_light_position = None
# LightingGradient.direction indicates the rotation degree of the light strip
lightinggradient_direction = None
# LightingGradient.max_brightness and LightingGradient.min_brightness set bounds for how much brightness change will happen
lightinggradient_max_brightness = 255
lightinggradient_min_brightness = 0
# LightingGradient.mode is linear or gaussian depending on how light should decay
lightinggradient_mode = random.choice(["linear_dynamic", "linear_static", "gaussian"])
# LightingGradient.linear_decay_rate is only valid in linear static mode
lightinggradient_linear_decay_rate = None
# LightingGradient.transparency gives the transparency of the input image
lightinggradient_transparency = None

# DirtyDrum.line_width_range determines the range from which drum line widths are sampled
dirtydrum_line_width_range = (2, 8)
# DirtyDrum.direction is 0 for horizontal, 1 for vertical, 2 for both
dirtydrum_direction = random.randint(0,2)
# DirtyDrum.noise_intensity changes how significant the effect is, recommended 0.8-1.0
dirtydrum_noise_intensity = 0.95
# DirtyDrum.ksize is a tuple of height/width pairs from which to sample kernel size
dirtydrum_ksize = (3, 3)
# DirtyDrum.sigmaX is the stdev of the kernel in the x direction
dirtydrum_sigmaX = 0

# SubleNoise.range gives the variation range for sampling noise
subtlenoise_range = 10

# Jpeg.quality_range determines the range from which to sample compression level
jpeg_quality_range = (25, 95)

# Markup.num_lines_range determines how many lines get marked up
markup_num_lines_range=(2, 7)
# Markup.length_range determines the relative length of the drawn effect
markup_length_range=(0.5, 1)
# Markup.thickness_range determines the thickness of the drawn effect
markup_thickness_range=(1, 3)
# Markup.type determines the style of effect
markup_type=random.choice(["strikethrough", "crossed", "highlight", "underline"])
# Markup.color is the color of the ink used to markup
markup_color=(random.randint(0,256),
              random.randint(0,256),
              random.randint(0,256))
# Markup.single_word_mode determines whether to draw across multiple words
markup_single_word_mode=random.choice([True, False])
# Markup.repetitions determines the number of times the effect is drawn
markup_repetitions=random.randint(1,5)

# PencilScribbles.size_range determines the size of scribbles to draw
pencilscribbles_size_range=(250, 400)
# PencilScribbles.count_range determines how many scribbles to draw
pencilscribbles_count_range=(1, 10)
# PencilScribbles.stroke_count_range determines how many strokes per scribble
pencilscribbles_stroke_count_range=(3, 6)
# PencilScribbles.thickness_range determines how thick strokes are
pencilscribbles_thickness_range=(2, 6)
# PencilScribbles.brightness_change is the brightness value of each stroke
pencilscribbles_brightness_change=random.randint(0,128)

# BindingsAndFasteners.overlay_types can be min, max, or mix
bindingsandfasteners_overlay_types = random.choice([
    "min", "max", "mix", "normal",
    "lighten", "darken", "addition", "subtract",
    "difference", "screen", "dodge", "multiply",
    "divide", "hard_light", "grain_extract",
    "grain_merge", "overlay"
])
# BindingsAndFasteners.foreground is the path to fg image or the image itself
bindingsandfasteners_foreground = None
# BindingsAndFasteners.effect_type is "punch_holes", "binding_holes", or "clips"
bindingsandfasteners_effect_type = random.choice(["punch_holes", "binding_holes", "clips"])
# BindingsAndFasteners.ntimes gives how many fg images to draw
bindingsandfasteners_ntimes = 3
# BindingsAndFasteners.nscales is the scale of the fg image size
bindingsandfasteners_nscales = (1,1)
# BindingsAndFasteners.edge gives the edge to place the images on
bindingsandfasteners_edge = random.choice(["left", "top", "bottom", "right"])
# BindingsAndFasteners.edge_offset is how far from the page edge to draw
bindingsandfasteners_edge_offset = 50

# BadPhotoCopy.mask is a mask of noise to generate the effect with
badphotocopy_mask=None
# BadPhotoCopy.noise_type determines which mask pattern to use
badphotocopy_noise_type=random.randint(1,8)
# BadPhotoCopy.noise_side determines where to add noise
badphotocopy_noise_side=random.choice([
            "random",
            "left",
            "right",
            "top",
            "bottom",
            "top_left",
            "top_right",
            "bottom_left",
            "bottom_right",
        ])
# BadPhotoCopy.noise_iteration determines how many times to apply noise in the mask
badphotocopy_noise_iteration=(1, 1)
# BadPhotoCopy.noise_size determines the scale of noise in the mask
badphotocopy_noise_size=(1, 1)
# BadPhotoCopy.noise_value determines the intensity of the noise
badphotocopy_noise_value=(30, 60)
# BadPhotoCopy.noise_sparsity determines the sparseness of noise
badphotocopy_noise_sparsity=(0.4, 0.6)
# BadPhotoCopy.noise_concentration determines the concentration of noise
badphotocopy_noise_concentration=(0.4, 0.6)
# BadPhotoCopy.blur_noise determines whether or or not to add blur
badphotocopy_blur_noise=random.choice([True,False])
# BadPhotoCopy.blur_noise_kernel gives the dimensions for the noise kernel
badphotocopy_blur_noise_kernel=(5, 5)
# BadPhotoCopy.wave_pattern enables the wave pattern in the noise mask
badphotocopy_wave_pattern=random.choice([True,False])
# BadPhotoCopy.edge_effect adds the Sobel edge effect to the noise mask
badphotocopy_edge_effect=random.choice([True,False])

# Gamma.range is an interval from which to sample a gamma shift
gamma_range = (0.5, 1.5)

# Geometric.scale is a pair determining how to scale the image
geometric_scale = (1, 1)
# Geometric.translation is a pair determining where to translate the image
geometric_translation = (0, 0)
# Geometric.fliplr flips the image left and right
geometric_fliplr = random.choice([0,1])
# Geometric.flipud flips the image up and down
geometric_flipud = random.choice([0,1])
# Geometric.crop is a tuple of four points giving the corners of a crop region
geometric_crop = ()
# Geometric.rotate_range is a pair determining the rotation angle sample range
geometric_rotate_range = (0, 0)

# Faxify.scale_range is a pair of ints determining the scaling magnitude
faxify_scale_range=(1, 1)
# Faxify.monochrome determines whether the image will get the halftone effect
faxify_monochrome=random.choice([True,False])
# Faxify.monochrome_method is the binarization method for applying the effect
faxify_monochrome_method=random.choice(["Otsu", "Simple", "Adaptive"])
# Faxify.adaptive_method decides how the threshold is calculated
faxify_adaptive_method=random.choice([
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.ADAPTIVE_THRESH_MEAN_C
    ])
# Faxify.monochrome_threshold is the simple binarization threshold value
faxify_monochrome_threshold=127
# Faxify.invert determines whether to invert the grayscale value in halftone
faxify_invert=1
# Faxify.half_kernel_size is half the Gaussian kernel size for halftone
faxify_half_kernel_size=2
# Faxify.angle is the angle of the halftone effect
faxify_angle=45
# Faxify.sigma is the sigma value of the Gaussian kernel in the halftone effect
faxify_sigma=2

################################################################################
# PIPELINE
#
# The default Augraphy pipeline is defined in parametric form here.
################################################################################

ink_phase = [
    Dithering(dithering_dither_type,
              dithering_order,
              p=0.2),

    InkBleed(inkbleed_intensity_range,
             inkbleed_color_range,
             inkbleed_kernel_size,
             inkbleed_severity,
             p=1),

    BleedThrough(bleedthrough_intensity_range,
                 bleedthrough_color_range,
                 bleedthrough_ksize,
                 bleedthrough_sigmaX,
                 bleedthrough_alpha,
                 bleedthrough_offsets,
                 p=0.5),

    Letterpress(letterpress_n_samples,
                letterpress_n_clusters,
                letterpress_std_range,
                letterpress_value_range,
                letterpress_value_threshold_range,
                letterpress_blur,
                p=0.5),

    OneOf(
        [
            LowInkRandomLines(lowinkrandomlines_count_range,
                              lowinkrandomlines_use_consistent_lines),

            LowInkPeriodicLines(lowinkperiodiclines_count_range,
                                lowinkperiodiclines_period_range,
                                lowinkperiodiclines_use_consistent_lines),
        ],
    ),
]

paper_phase = [
    PaperFactory(paperfactory_tile_texture_shape,
                 paperfactory_texture_path,
                 p=0.5),
    OneOf(
        [
            AugmentationSequence(
                [
                    NoiseTexturize(noisetexturize_sigma_range,
                                   noisetexturize_sigma_range),

                    BrightnessTexturize(brightnesstexturize_range,
                                        brightnesstexturize_deviation),
                ],
            ),
            AugmentationSequence(
                [
                    BrightnessTexturize(brightnesstexturize_range,
                                        brightnesstexturize_deviation),
                    NoiseTexturize(noisetexturize_sigma_range,
                                   noisetexturize_sigma_range),
                ],
            ),
        ],
        p=0.5,
    ),

    Brightness(brightness_range,
               p=0.5),
]

post_phase = [
    BrightnessTexturize(brightnesstexturize_range,
                        brightnesstexturize_deviation,
                        p=0.5),

    OneOf(
        [
            PageBorder(pageborder_side,
                       pageborder_width_range,
                       pageborder_pages),
            DirtyRollers(dirtyrollers_line_width_range,
                         dirtyrollers_scanline_type)
        ],
        p=0.5),

    OneOf(
        [
            LightingGradient(lightinggradient_light_position,
                             lightinggradient_max_brightness,
                             lightinggradient_min_brightness,
                             lightinggradient_mode,
                             lightinggradient_linear_decay_rate,
                             lightinggradient_transparency),
            Brightness(brightness_range)
        ],
        p=0.5),

    DirtyDrum(dirtydrum_line_width_range,
              dirtydrum_direction,
              dirtydrum_noise_intensity,
              dirtydrum_ksize,
              dirtydrum_sigmaX,
              p=0.5),

    SubtleNoise(subtlenoise_range,
                p=0.5),

    Jpeg(jpeg_quality_range,
         p=0.5),

    Markup(num_lines_range=markup_num_lines_range,
           markup_length_range=markup_length_range,
           markup_thickness_range=markup_thickness_range,
           markup_type=markup_type,
           markup_color=markup_color,
           single_word_mode=markup_single_word_mode,
           repetitions=markup_repetitions,
           p=0.5),

    PencilScribbles(size_range=pencilscribbles_size_range,
                    count_range=pencilscribbles_count_range,
                    stroke_count_range=pencilscribbles_stroke_count_range,
                    thickness_range=pencilscribbles_thickness_range,
                    brightness_change=pencilscribbles_brightness_change,
                    p=0.5),

    BindingsAndFasteners(bindingsandfasteners_overlay_types,
                         bindingsandfasteners_foreground,
                         bindingsandfasteners_effect_type,
                         bindingsandfasteners_ntimes,
                         bindingsandfasteners_nscales,
                         bindingsandfasteners_edge,
                         bindingsandfasteners_edge_offset,
                         p=0.5),

    BadPhotoCopy(mask=badphotocopy_mask,
                 noise_type=badphotocopy_noise_type,
                 noise_side=badphotocopy_noise_side,
                 noise_iteration=badphotocopy_noise_iteration,
                 noise_size=badphotocopy_noise_size,
                 noise_value=badphotocopy_noise_value,
                 noise_sparsity=badphotocopy_noise_sparsity,
                 noise_concentration=badphotocopy_noise_concentration,
                 blur_noise=badphotocopy_blur_noise,
                 blur_noise_kernel=badphotocopy_blur_noise_kernel,
                 wave_pattern=badphotocopy_wave_pattern,
                 edge_effect=badphotocopy_edge_effect,
                 p=0.5),

    Gamma(gamma_range,
          p=0.5),

    Geometric(geometric_scale,
              geometric_translation,
              geometric_fliplr,
              geometric_flipud,
              geometric_crop,
              geometric_rotate_range,
              p=0.5),

    Faxify(scale_range=(1, 1),
           monochrome=faxify_monochrome,
           monochrome_method=faxify_monochrome_method,
           adaptive_method=faxify_adaptive_method,
           monochrome_threshold=faxify_monochrome_threshold,
           invert=faxify_invert,
           half_kernel_size=faxify_half_kernel_size,
           angle=faxify_angle,
           sigma=faxify_sigma,
           p=0.5),
]

def get_pipeline():
    """ This makes things easier."""
    return AugraphyPipeline(ink_phase,paper_phase,post_phase)
