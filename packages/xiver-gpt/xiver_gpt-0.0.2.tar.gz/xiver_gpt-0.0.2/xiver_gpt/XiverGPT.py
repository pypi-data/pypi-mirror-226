from typing import Any, Generator
import inspect

import g4f

from .exceptions import NoProvider

__all__ = ("XiverGPT",)


PROVIDERS_BLACKLIST = (
    g4f.Provider.Aichat,
    g4f.Provider.Acytoo,
    g4f.Provider.Ails,
    g4f.Provider.ChatgptAi,
)


class XiverGPT:
    """The main class of xiver_gpt lib
    """
    def __init__(self, *, g4f_model: g4f.models.Model = g4f.models.gpt_4, \
                 g4f_provider: Any | None = None, \
                 stream: bool = False) -> None:

        self.g4f_worked_providers = []

        # Support vars
        self.__provider_num = 0

        self.g4f_model      = g4f_model
        self.g4f_provider   = g4f_provider

        self.stream = stream

        self.providers  = [cls_obj for _, cls_obj in inspect.getmembers(g4f.Provider) if inspect.isclass(cls_obj)]
        self.models     = [cls_obj for _, cls_obj in inspect.getmembers(g4f.models) if inspect.isclass(cls_obj)]

        try:
            self.models.remove(type)
            self.providers.remove(type)

            self.providers.remove(g4f.Provider.base_provider)
        except ValueError:
            pass

        self.auto_update_provider()

    def auto_update_provider(self) -> None:  # pylint: disable=too-many-branches
        if self.g4f_provider:
            try:
                response = g4f.ChatCompletion.create(model=self.g4f_model, provider=self.g4f_provider, messages=[
                                            {"role": "user", "content": "Hello world"}], stream=self.stream)

                if 'is not working' in response or \
                        'error' in response or \
                        not response:
                    raise
            except Exception as exc:
                raise NoProvider(self.g4f_model) from exc

            self.g4f_worked_providers.append(self.g4f_provider)
            return

        work_providers = []
        for provider in self.providers:

            if not provider.working or provider.supports_stream < self.stream or \
                provider in PROVIDERS_BLACKLIST:
                continue

            try:
                response = self.__create_response(self.g4f_model, provider, "Hello world", self.stream)

                res = response if not self.stream else ' '.join([i for i in response])

                if 'is not working' in res or \
                    'error' in res or \
                        not res:
                    raise
                work_providers.append(provider)
            except:  # pylint: disable=bare-except
                pass
        
        print(f'{work_providers=}')

        for prov in work_providers:
            try:
                response = self.__create_response(self.g4f_model, prov, "Hello world", self.stream)

                res = ''
                for i in response:
                    res.join(i)

                if 'error' not in res:
                    self.g4f_worked_providers.append(prov)
            except:  # pylint: disable=bare-except
                pass

        if not self.g4f_worked_providers:
            raise NoProvider(self.g4f_model)

    def create_response(self, message: str, stream: bool = False) -> str | Generator:
        response = None
        
        try:
            response = self.__create_response(
                self.g4f_model,
                self.g4f_worked_providers[self.__provider_num],
                message,
                stream,
            )
        except: # pylint: disable=bare-except
            self.__provider_num += 1

        while not response or '"error":' in response:
            self.__provider_num += 1
            if self.__provider_num > len(self.g4f_worked_providers):
                self.__provider_num = 0

            try:
                response = self.__create_response(
                    self.g4f_model,
                    self.g4f_worked_providers[self.__provider_num],
                    message,
                    stream,
                )
            except: # pylint: disable=bare-except
                self.__provider_num += 1

        return response

    def __create_response(self, model, provider, message, stream) -> Any:
        return g4f.ChatCompletion.create(
            model=model,
            provider=provider,
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            stream=stream,
        )
