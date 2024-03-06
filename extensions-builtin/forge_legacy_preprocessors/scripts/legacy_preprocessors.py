# This is a python script to convert all old preprocessors to new format.
# However, the old preprocessors are not very memory effective
# and eventually we should move all old preprocessors to new format manually
# see also the forge_preprocessor_normalbae/scripts/preprocessor_normalbae for
# how to make better implementation of preprocessors.
# No newer preprocessors should be written in this legacy way.

# Never add new leagcy preprocessors please.
# The new forge_preprocessor_normalbae/scripts/preprocessor_normalbae
# is much more effective and maintainable


import contextlib

from annotator.util import HWC3
from modules_forge.ops import automatic_memory_management
from legacy_preprocessors.preprocessor_compiled import legacy_preprocessors
from modules_forge.supported_preprocessor import Preprocessor, PreprocessorParameter
from modules_forge.shared import add_supported_preprocessor


###

# This file has lots of unreasonable historical designs and should be viewed as a frozen blackbox library.

# If you want to add preprocessor,
# please instead look at `extensions-builtin/forge_preprocessor_normalbae/scripts/preprocessor_normalbae`
# If you want to use preprocessor,
# please instead use `from modules_forge.shared import supported_preprocessors`
# and then use any preprocessor like: depth_midas = supported_preprocessors['depth_midas']

# Please do not hack/edit/modify/rely-on any codes in this file.

# Never use methods in this file to add anything!
# This file will be eventually removed but the workload is super high and we need more time to do this.

###


class LegacyPreprocessor(Preprocessor):
    def __init__(self, legacy_dict):
        super().__init__()
        self.name = legacy_dict['label']
        self.call_function = legacy_dict['call_function']
        self.unload_function = legacy_dict['unload_function']
        self.managed_model = legacy_dict['managed_model']
        self.do_not_need_model = legacy_dict['model_free']
        self.show_control_mode = not legacy_dict['no_control_mode']
        self.sorting_priority = legacy_dict['priority']
        self.tags = legacy_dict['tags']

        filters_aliases = {
            'instructp2p': ['ip2p'],
            'segmentation': ['seg'],
            'normalmap': ['normal'],
            't2i-adapter': ['t2i_adapter', 't2iadapter', 't2ia'],
            'ip-adapter': ['ip_adapter', 'ipadapter'],
            'openpose': ['openpose', 'densepose'],
            'instant-iD': ['instant_id', 'instantid'],
        }

        if legacy_dict.get('use_soft_projection_in_hr_fix', False):
            self.use_soft_projection_in_hr_fix = True

        self.model_filename_filters = []
        for tag in self.tags:
            tag_lower = tag.lower()
            self.model_filename_filters.append(tag_lower)
            self.model_filename_filters += filters_aliases.get(tag_lower, [])

        if legacy_dict['resolution'] is None:
            self.resolution = PreprocessorParameter(visible=False)
        else:
            legacy_dict['resolution']['label'] = 'Resolution'
            legacy_dict['resolution']['step'] = 8
            self.resolution = PreprocessorParameter(**legacy_dict['resolution'], visible=True)

        if legacy_dict['slider_1'] is None:
            self.slider_1 = PreprocessorParameter(visible=False)
        else:
            self.slider_1 = PreprocessorParameter(**legacy_dict['slider_1'], visible=True)

        if legacy_dict['slider_2'] is None:
            self.slider_2 = PreprocessorParameter(visible=False)
        else:
            self.slider_2 = PreprocessorParameter(**legacy_dict['slider_2'], visible=True)

        if legacy_dict['slider_3'] is None:
            self.slider_3 = PreprocessorParameter(visible=False)
        else:
            self.slider_3 = PreprocessorParameter(**legacy_dict['slider_3'], visible=True)

    def __call__(self, input_image, resolution, slider_1=None, slider_2=None, slider_3=None, **kwargs):
        # Legacy Preprocessors does not have slider 3
        del slider_3

        if self.unload_function is not None or self.managed_model is not None:
            context = automatic_memory_management
        else:
            context = contextlib.nullcontext

        with context():
            result, is_image = self.call_function(img=input_image, res=resolution, thr_a=slider_1, thr_b=slider_2, **kwargs)

        if is_image:
            result = HWC3(result)

        if self.unload_function is not None:
            self.unload_function()

        return result


for name, data in legacy_preprocessors.items():
    p = LegacyPreprocessor(data)
    p.name = name
    # Invert should not match any particular model.
    if "invert" in name:
        p.model_filename_filters = []
    add_supported_preprocessor(p)
