from abc import ABC, abstractmethod




class VectorStoreService(ABC):

    @abstractmethod
    def get_vector_store(self) -> object:
        pass

    @abstractmethod
    def load_data(self, csv_file):
        pass

