# -*- coding: utf-8 -*-


def extract_form(response, form_xpath):
    dados = {}
    form = response.xpath(form_xpath)
    elementos = form.xpath('.//*[name()="input" or name()="select"]')
    for elemento in elementos:
        nome = ''.join(elemento.xpath('./@name').extract())
        valor = ''.join(elemento.xpath('./@value').extract())
        if nome:
            dados[nome] = valor
    return dados
