from enums import SpiderStatus
from enums import InstanciaStatus


ESTADOS_BRASIL = [
    'GO', 'MT', 'MS', 'DF', 'AM', 'AC', 'RO', 'RR',
    'AP', 'TO', 'PA', 'MA', 'PI', 'CE', 'RN', 'PB',
    'PE', 'SE', 'AL', 'BA', 'SP', 'MG', 'RJ', 'ES',
    'PR', 'SC', 'RS']

DEFAULT_COVERAGE = {
    'status': SpiderStatus.NAO_IMPLEMENTADO,
    'captcha': False,
    'arquivos': False,
    '1-grau-fisico': InstanciaStatus.NAO_IMPLEMENTADO,
    '2-grau-fisico': InstanciaStatus.NAO_IMPLEMENTADO,
    '1-grau-eletronico': InstanciaStatus.NAO_IMPLEMENTADO,
    '2-grau-eletronico': InstanciaStatus.NAO_IMPLEMENTADO,
    'jec-1-grau-fisico': InstanciaStatus.NAO_IMPLEMENTADO,
    'jec-2-grau-fisico': InstanciaStatus.NAO_IMPLEMENTADO,
    'jec-1-grau-eletronico': InstanciaStatus.NAO_IMPLEMENTADO,
    'jec-2-grau-eletronico': InstanciaStatus.NAO_IMPLEMENTADO,
}
