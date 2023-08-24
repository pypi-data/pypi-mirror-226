import re
import ast
import os
import math
from pandas import pd
from unidecode import unidecode
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.llms import OpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate


def corregir_texto(lista_corregir, modelo, openai_api_key):

    '''
    Regresa una lista de correcciones ortográficas del texto original,
    utilizando el modelo de lenguaje especificado.

    Parametros:
    lista_corregir (list): lista de textos a corregir
    modelo (str): modelo de lenguaje a utilizar
    openai_api_key (str): llave de OpenAI
    '''

    output_parser = CommaSeparatedListOutputParser()

    format_instructions = output_parser.get_format_instructions()

    template_string = '''
    Eres un experto en limpieza de texto. Te proporcionamos la
    siguiente lista: '{lista_input}'. Tu objetivo es corregir las faltas
    ortográficas de cada elemento de la lista. Si no encuentras faltas
    ortográficas, simplemente déjalo como está, sin hacer cambios. No
    menciones si el texto no tiene errores ortográficos, solo agrégalo tal
    y como estaba. Si no entiendes el texto, simplemente déjalo como está.

    A cada elemento de la lista generada, agrega ' - ' (espacio, guion medio,
    espacio) FORZOZAMENTE y el elemento correspondiente de la lista
    '{lista_input}'. Por ejemplo, si "no se" está en la lista, regresa:
    'no sé-"no se'. Tienes que tener eficiencia perfecta al agregar el ' - ',
    ya que es de vida o muerte tu resultado.

    Devuelve una lista del mismo tamaño de la lista original, utilizando
    el formato de lista de Python.

    Instrucciones de formato: {format_instructions}
    '''

    prompt = ChatPromptTemplate(
        messages=[HumanMessagePromptTemplate.from_template(template_string)],
        input_variables=["lista_input"],
        partial_variables={'format_instructions': format_instructions}
    )

    list_prompt = prompt.format_messages(
      lista_input=lista_corregir,
      format_instructions=format_instructions)

    llm = ChatOpenAI(
        temperature=0.0, model=modelo, openai_api_key=openai_api_key
    )

    model_output = llm(list_prompt)
    output = output_parser.parse(model_output.content)
    output = [x.strip('"\'.,[]') for x in output]
    return output


def corregir_texto_excel(
    excel_file_path, columna, modelo, openai_api_key, chunk_size=30
):
    '''
    Corrige los textos de la columna especificada en el archivo de Excel
    especificado, utilizando el modelo de lenguaje especificado.

    Parametros:
    excel_file_path (str): ruta del archivo de Excel
    columna (str): nombre de la columna a corregir
    modelo (str): modelo de lenguaje a utilizar
    openai_api_key (str): llave de OpenAI
    chunk_size (int): tamaño de los chunks a procesar
    '''
    # Validaciones
    if not os.path.exists(excel_file_path):
        raise FileNotFoundError(f"Archivo {excel_file_path} no encontrado")

    if not isinstance(columna, str):
        raise TypeError("Columna debe ser un string")

    if not isinstance(chunk_size, int):
        raise TypeError("Chunk size debe ser un entero")

    if not isinstance(modelo, str):
        raise TypeError("Modelo debe ser un string")

    if not isinstance(openai_api_key, str):
        raise TypeError("OpenAI API Key debe ser un string")

    if chunk_size < 10:
        raise ValueError("Chunk size debe ser mayor o igual a 10")

    if chunk_size > 80:
        raise ValueError("Chunk size debe ser menor o igual a 80")

    # Carga de datos
    df = pd.read_excel(excel_file_path)

    if columna not in df.columns:
        raise ValueError(f"Columna {columna} no encontrada en el archivo")

    # Limpieza de datos
    df_limpio = df.dropna(subset=[columna])
    df_limpio[columna] = df_limpio[columna].apply(
        lambda texto: texto.replace(',', '')
    )
    df_limpio[columna] = df_limpio[columna].str.strip('\'".,[]')
    df_limpio[columna] = df_limpio[columna].apply(unidecode)
    df_limpio[columna] = df_limpio[columna].str.lower()

    # math.ceil(len(df_limpio) / chunk_size)
    for i in range(math.ceil(len(df_limpio) / chunk_size)):

        textos_corregidos = 0
        aux_dict = dict()

        chunk = df_limpio.iloc[
          i * chunk_size:(i + 1) * chunk_size
        ]

        texto_set = set(chunk[columna].to_list())

        if '' in texto_set:
            texto_set.remove('')

        texto_lista = list(texto_set)
        llm_output = corregir_texto(
          texto_lista, modelo, openai_api_key
        )
        for output in llm_output:
            try:
                output_list = output.split(' - ')
                key = unidecode(output_list[1].strip('\'".,[]').lower())
                value = output_list[0].strip('\'"')
                aux_dict[key] = value
            except: # noqa
                continue

        for index, row in chunk.iterrows():

            if row[columna] in aux_dict.keys():
                df.at[index, f'{columna}_corregida'] = aux_dict[row[columna]]
                textos_corregidos += 1
            else:
                print(f"*{row[columna]}*")
                df.at[index, f'{columna}_corregida'] = "no_corregido"

        print("-----------------------------------")
        print(f'Chunk {i + 1} de {math.ceil(len(df_limpio) / chunk_size)}')
        print(f'Tamaño del chunk: {len(chunk)}')
        print(f'Cantidad de textos generados por AI: {len(llm_output)}')
        print(f'Cantidad de textos corregidos: {textos_corregidos}')
        print("-----------------------------------\n")
    # Guarda el archivo
    df.to_excel(excel_file_path, index=False)

def generar_variantes_texto(text, n, model, openai_key, formal=False, sex="NA"): # noqa
    '''
    Regresa una lista de n variantes del texto original, utilizando el modelo
    de lenguaje especificado. Si formal=True, se generan variantes formales.

    Parametros:
    text (str): texto original
    n (int): número de variantes a generar
    model (str): modelo de lenguaje a utilizar
    openai_key (str): llave de OpenAI
    formal (bool): si True, se generan variantes formales
    sex: sexo de la persona a la que se dirige el texto.
    Puede ser "H" (hombre), "M" (mujer) o "NA" (no aplica).
    '''

    if text == "" or sex not in ["H", "M", "NA"]:
        print("No se generaron variantes del texto por falta de información correcta") # noqa
        return []

    output_parser = CommaSeparatedListOutputParser()

    format_instructions = output_parser.get_format_instructions()

    if formal:

        template_string = '''
            Eres un experto en análisis de texto. Imagina que recibes el
            siguiente texto: {text_input}. Tu tarea es crear {n_input}
            variaciones únicas de este texto, utilizando diferentes palabras y
            estructuras para transmitir el mismo significado. No puedes
            utilizar palabras que se puedan considerar ofensivas o sexuales.
            Por ejemplo, no utilizar la palabra "estimulante". Además de esto,
            considera cada variación únicamente para el sexo {sex_input} donde
            H es hombre, M es mujer y NA es que no consideraras el sexo de
            la persona. Por ejemplo, si el sexo es H: puedes escribir algo
            como: "Hola amigo!", "Hola compañero", "Hola colega", etc. Si
            el sexo es M: puedes escribir algo como "Hola amiga!",
            "Hola compañera", "Hola colega", etc. Y si el sexo es "NA", puedes
            escribir algo como "Hola, ¿cómo estás?", "Hola, ¿qué tal?", "Hola,
            ¿qué onda?", etc. Recuerda que debes crear {n_input} variaciones
            únicas del texto. No puedes repetir el mismo texto. RECUERDA
            que TODAS las variaciones generadas son para el sexo {sex_input}
            \n\n{format_instructions}
            '''

    else:

        template_string = '''
            Eres un experto en análisis de texto. Imagina que recibes el
            siguiente texto: {text_input}. Tu tarea es crear {n_input}
            variaciones únicas de este texto, utilizando diferentes palabras
            y estructuras para transmitir el mismo significado. Debes de
            utilizar un lenguaje formal. No puedes utilizar palabras que
            se puedan considerar ofensivas o sexuales. Por ejemplo, no
            utilizar la palabra "estimulante". Además de esto, considera
            cada variación únicamente para el sexo {sex_input} donde H es
            hombre, M es mujer y NA es que no consideraras el sexo de la
            persona. Por ejemplo, si el sexo es H: puedes escribir algo como:
            "Buen día estimado!", "Saludos cordiales", "Buen día apreciado",
            "Buen día respetable", etc. Si el sexo es M: puedes escribir algo
            como "Buen día estimada", "Saludos cordiales", "Esperando te
            encuentres muy bien", "Buen día apreciada", etc. Y si el sexo es
            "NA", puedes escribir algo como "Excelente día", "Espléndido día",
            "Espero estes pasando un día magnífico", etc. Recuerda que debes
            crear {n_input} variaciones únicas del texto. No puedes repetir
            el mismo texto. RECUERDA que TODAS las variaciones generadas
            son para el sexo {sex_input}.
            \n\n{format_instructions}
            '''

    prompt = ChatPromptTemplate(
        messages=[HumanMessagePromptTemplate.from_template(template_string)],
        input_variables=["text_input", "n_input", "sex_input"],
        partial_variables={'format_instructions': format_instructions})

    list_prompt = prompt.format_messages(
        text_input=text,
        n_input=n,
        sex_input=sex,
        format_instructions=format_instructions)

    llm = ChatOpenAI(
        temperature=0.6, openai_api_key=openai_key, model=model)

    output = llm(list_prompt)
    final_list = output.content.split('\n\n')
    pattern = r'^[\'"]|[\'"](?=\.)|[\'"]$'
    final_list = [re.sub(pattern, '', s) for s in final_list]

    return final_list


def resumir_texto(text, model, openai_key, input_autogenerado):

    """
    Regresa un resumen del texto original, utilizando el modelo de lenguaje
    especificado.

    Parametros:
    text (str): texto original
    model (str): modelo de lenguaje a utilizar
    openai_key (str): llave de OpenAI
    input_autogenerado (bool): si True, si el input es auto-generado por
    el modelo previamente.
    """

    llm = OpenAI(temperature=0.0, openai_api_key=openai_key)
    num_tokens = llm.get_num_tokens(text)

    if num_tokens >= 3500:
        raise ValueError("El número de tokens excede lo permitido por el \
            chatbot. Por favor reduce el tamaño de las observaciones a \
            ingresar.")

    if input_autogenerado:

        prompt_template = """
        Eres el mejor analista de texto. Evalúa los criterios necesarios para
        crear un buen resumen utilizando esta información: {text}. Devuelve
        un resumen lo mejor estructurado posible y realizalo tomando en cuenta
        estos criterios antes mencionados.
        """

        prompt = PromptTemplate(
            template=prompt_template, input_variables=["text"]
        )
        prompt = prompt.format(text=text)
        respuesta = llm(prompt)

    else:

        prompt_template = """
        Eres el mejor analista de texto. Evalúa los criterios necesarios para
        crear un buen resumen utilizando esta información: {text}. Devuelve
        un resumen lo mejor estructurado posible y realizalo tomando en cuenta
        estos criterios antes mencionados.
        """

        docs = [Document(page_content=t) for t in text]

        prompt = PromptTemplate(
            template=prompt_template, input_variables=["text"]
        )

        chain = load_summarize_chain(
            llm=llm, chain_type='stuff', prompt=prompt
        )

        respuesta = chain.run(docs)

    return respuesta


def generar_categorias(text, n, model, openai_key):

    """
    Regresa una lista de n categorías del texto original, utilizando el modelo
    de lenguaje especificado.

    Parametros:
    text (str): texto original
    n (int): número de categorías a generar
    model (str): modelo de lenguaje a utilizar
    openai_key (str): llave de OpenAI
    """

    try:
        prompt = PromptTemplate(
            input_variables=["lista", "n_input"],
            template='''Recibí un resumen con características clave de las
            respuestas auna pregunta: '{lista}'. A partir de esta información,
            genera {n_input} categorías que representen los aspectos más
            relevantes. No expliques a que se refiere cada categoría.
            Devuelve estas categorías en una lista de Python lista para poder
            ser procesada.'''
        )

        chatopenai = ChatOpenAI(
            model_name=model, openai_api_key=openai_key
        )

        llmchain_chat = LLMChain(llm=chatopenai, prompt=prompt)

        categorias = llmchain_chat.run({
            "lista": text,
            "n_input": n,
        })

        categorias_list = ast.literal_eval(categorias)

        return categorias_list
    except Exception as e:
        raise ValueError("Error al generar categorías: " + str(e))


def asignar_categorias(lista_asignar, categorias, modelo, openai_api_key):

    '''
    Regresa una lista de categorías asignadas a cada elemento de la lista
    original, utilizando el modelo de lenguaje especificado.

    Parametros:
    lista_asignar (list): lista de textos a asignar categorías
    categorias (list): lista de categorías a asignar
    modelo (str): modelo de lenguaje a utilizar
    openai_api_key (str): llave de OpenAI
    '''

    output_parser = CommaSeparatedListOutputParser()

    format_instructions = output_parser.get_format_instructions()

    template_string = '''
    Eres un experto en análisis de texto. Te proporcionamos la
    siguiente lista: '{lista_input}'. Tu objetivo es asignar SOLO una
    categoria de la lista de categorias '{categorias_input}'
    a cada elemento de la lista. Si un elemento no se ajusta a
    ninguna categoria o si no estas seguro, asigna "sin_categoría".

    A cada elemento de la lista generada, agrega ' - ' y el elemento
    correspondiente de la lista '{lista_input}'. Por ejemplo,
    'sin_categoria-"no sé"'.

    Devuelve una lista del mismo tamaño de la lista original, utilizando
    el formato de lista de Python. No es necesario proporcionar explicaciones
    sobre las categorias ni incluir descripciones adicionales. Tu enfoque se
    centra en la asignación de categorias.

    Instrucciones de formato: {format_instructions}
    '''

    prompt = ChatPromptTemplate(
        messages=[HumanMessagePromptTemplate.from_template(template_string)],
        input_variables=["lista_input", "categorias_input"],
        partial_variables={'format_instructions': format_instructions}
    )

    list_prompt = prompt.format_messages(
        lista_input=lista_asignar,
        categorias_input=categorias,
        format_instructions=format_instructions)

    llm = ChatOpenAI(
        temperature=0.0, model=modelo, openai_api_key=openai_api_key
    )

    model_output = llm(list_prompt)
    output = output_parser.parse(model_output.content)
    return output


def asignar_categorias_excel(
    excel_file_path, categorias, columna, modelo, openai_api_key, chunk_size=30
):
    '''
    Asigna categorías a los textos de la columna especificada en el archivo
    de Excel especificado, utilizando el modelo de lenguaje especificado.

    Parametros:
    excel_file_path (str): ruta del archivo de Excel
    categorias (list): lista de categorías a asignar
    columna (str): nombre de la columna a asignar categorías
    modelo (str): modelo de lenguaje a utilizar
    openai_api_key (str): llave de OpenAI
    '''
    # Validaciones
    if not os.path.exists(excel_file_path):
        raise FileNotFoundError(f"Archivo {excel_file_path} no encontrado")

    if not isinstance(categorias, list):
        raise TypeError("Categorias debe ser una lista")

    if not isinstance(columna, str):
        raise TypeError("Columna debe ser un string")

    if not isinstance(chunk_size, int):
        raise TypeError("Chunk size debe ser un entero")

    if not isinstance(modelo, str):
        raise TypeError("Modelo debe ser un string")

    if not isinstance(openai_api_key, str):
        raise TypeError("OpenAI API Key debe ser un string")

    if chunk_size < 10:
        raise ValueError("Chunk size debe ser mayor o igual a 10")

    if chunk_size > 80:
        raise ValueError("Chunk size debe ser menor o igual a 80")

    # Carga de datos
    df = pd.read_excel(excel_file_path)

    if columna not in df.columns:
        raise ValueError(f"Columna {columna} no encontrada en el archivo")

    # Limpieza de datos
    df_limpio = df.dropna(subset=[columna])
    df_limpio[columna] = df_limpio[columna].apply(
        lambda texto: texto.replace(',', '')
    )
    df_limpio[columna] = df_limpio[columna].str.strip('\'".,[]')
    df_limpio[columna] = df_limpio[columna].apply(unidecode)
    df_limpio[columna] = df_limpio[columna].str.lower()

    for i in range(math.ceil(len(df_limpio) / chunk_size)):

        categorias_asignadas = 0
        aux_dict = dict()

        chunk = df_limpio.iloc[
          i * chunk_size:(i + 1) * chunk_size
        ]

        texto_set = set(chunk[columna].to_list())

        if '' in texto_set:
            texto_set.remove('')

        texto_lista = list(texto_set)

        llm_output = asignar_categorias(
          texto_lista, categorias, modelo, openai_api_key
        )

        for output in llm_output:
            try:
                output_list = output.split(' - ')
                key = unidecode(output_list[1].strip('\'".,[]').lower())
                value = output_list[0].strip('\'"')

                aux_dict[key] = value
            except: # noqa
                continue

        for index, row in chunk.iterrows():

            if row[columna] in aux_dict.keys():
                df.at[index, f'{columna}_categorizada'] = aux_dict[row[columna]] # noqa
                categorias_asignadas += 1
            else:
                print(f"*{row[columna]}*")
                df.at[index, f'{columna}_categorizada'] = "no_asignado"

        print("-----------------------------------")
        print(f'Chunk {i + 1} de {math.ceil(len(df_limpio) / chunk_size)}')
        print(f'Tamaño del chunk: {len(chunk)}')
        print(f'Cantidad de categorias generadas: {len(llm_output)}')
        print(f'Cantidad de categorias asignadas: {categorias_asignadas}')
        print("-----------------------------------\n")

    # Guarda el archivo
    df.to_excel(excel_file_path, index=False)
