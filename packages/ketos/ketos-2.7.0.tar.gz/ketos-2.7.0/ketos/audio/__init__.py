from ketos.data_handling.parsing import parse_parameter
from ketos.audio.spectrogram import MagSpectrogram, PowerSpectrogram, MelSpectrogram, CQTSpectrogram
from ketos.audio.waveform import Waveform
from ketos.audio.gammatone import GammatoneFilterBank, AuralFeatures
from pathlib import Path
from zipfile import ZipFile
import importlib
import sys
import zipimport
import json

audio_representation_names_in_recipe = {'Waveform':Waveform,
                                        'MagSpectrogram':MagSpectrogram, 
                                        'PowerSpectrogram':PowerSpectrogram,
                                        'MelSpectrogram':MelSpectrogram,
                                        'CQTSpectrogram':CQTSpectrogram,
                                        'AuralFeatures': AuralFeatures,
                                        'GammatoneFilterBank': GammatoneFilterBank}

def load_audio_representation_from_file(model_file):
    """ Load the audio representation from a ketos (.kt) model file.
        
        Args:
            model_file:str
                Path to the ketos(.kt) file
                
        Raises:
            ValueError: If the audio representation configuration does not contain a valid value for the 'type' field.

        Returns:
            audio_repr: Returns a dictionary with the loaded audio representation.

    """
    audio_representations = [] # There can be multiple representations

    # First we need to get the recipe file to know which audio representation we are working with.
    path = Path(model_file)
    with ZipFile(path, 'r') as archive: # we dont need to extract from the zipfile, we can just load directly into memory
        audio_recipe_file = archive.open('audio_repr.json')
        json_content = json.load(audio_recipe_file)
        # the representations are stored in the files as: {rep: representation, rep2: representation_2}, 
        # but we dont need the name of the representation, so we are building a list as just: [representation, representation2]
        # We should change this in the rest of the code as it is not needed
        for _, representation in json_content.items(): 
            audio_representations.append(representation)
    
    # The script prioritizes custom audio representations over the default ones from ketos. So if the user defined a custom representation with the same name as a default one, it will prioritize the custom
    # if there is no custom representation it will attempt to load a default one
    for idx, representation in enumerate(audio_representations):
        try:
            # See docs https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
            module_name = "audio_representation" #The file name will always be audio_representation because this is how ketos saves it
            module_path = zipimport.zipimporter(path / "custom") # the folder name within the zip archive will always be custom
            spec = module_path.find_spec(module_name)

            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module # adding the module to the list of modules in sys
            spec.loader.exec_module(module) # actually load the module, this is equivalent to importing
            # Now we load the class
            audio_representation_class = getattr(module, representation['type'])
            audio_representations[idx]['type'] = audio_representation_class
        except AttributeError:
            # fallback to the dictionary
            try:
                # load the class from the default audio representations in ketos
                audio_representations[idx]['type'] = audio_representation_names_in_recipe[representation['type']]
            except KeyError as e:
                e.__suppress_context__ = True # we are supressing the first attribute error as it is not useful
                raise ValueError(f"The audio representation '{representation['type']}' is not a valid audio representation")
        
        # We now need to parse the string values in the representation to their proper units. 
        # ToDo: As we discuseed previously, we should use default units os htat we dont have to make this complicated parsing.
        for key,value in representation.items(): 
            audio_representations[idx][key] = parse_parameter(name=key, value=value)

    return audio_representations