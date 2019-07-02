from os.path import join
from gensim.models import Word2Vec

class Model(Word2Vec):

    @classmethod
    def load(cls, models_directory=None, filename=None):
        try:
            model = super(Model, cls).load(join(models_directory, filename))
            model.metadata = {
                'filename': filename
            }
        except OSError:
            model = Model()
            model.metadata = {
                'error': 'File not found: {}'.format(filename)
            }
        return model
