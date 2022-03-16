import logging
from asyncio import create_task
from bs4 import BeautifulSoup
import httpx


base_url = "https://www.urparts.com/index.cfm/page/catalogue"


async def fetch(url):
    """Returns bs4 instance with url content"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            return BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            logging.error(f"func_fetch unable to fetch {url}: {e}")
        return BeautifulSoup("", "html.parser")


async def get_manufacturers(url=base_url):
    """Returns a list of manufacturers"""
    doc = await fetch(url)
    parent_tag = doc.find("div", {"class": "c_container allmakes"})
    a_tags = parent_tag.find_all("a") if parent_tag else []
    return [link.get_text().strip() for link in a_tags]


async def get_machine_types(manufacturer, base_url=base_url):
    """Returns a list of machine-types for a given manufacturer"""
    doc = await fetch(f"{base_url}/{manufacturer}")
    parent_tag = doc.find("div", {"class": "c_container allmakes allcategories"})
    a_tags = parent_tag.find_all("a") if parent_tag else []
    return [link.get_text().strip()[:-6] for link in a_tags]


async def get_machine_models(manufacturer, machine_type, base_url=base_url):
    """Returns a list of machine-models for a given manufacturer and machine type"""
    doc = await fetch(f"{base_url}/{manufacturer}/{machine_type} Parts")
    parent_tag = doc.find("div", {"class": "c_container allmodels"})
    a_tags = parent_tag.find_all("a") if parent_tag else []
    return [link.get_text().strip() for link in a_tags]


async def get_parts(model_id, manufacturer, machine_type, machine_model):
    """Returns a list of machine parts for a given machine-model of manufacturer's machine type

    Returns:
        list: [ model_id, manufacturer, machine_type, machine_model,[(part_number, category), ..]]
    """
    doc = await fetch(f"{base_url}/{manufacturer}/{machine_type} Parts/{machine_model}")
    parent_tag = doc.find("div", {"class": "c_container allparts"})
    a_tags = parent_tag.find_all("a") if parent_tag else []

    # Using Set to remove duplicate
    part_numbers_and_category = set()

    for link in a_tags:
        number, *category = link.get_text().strip().split(" - ", 1)
        category = category[0] if category else None
        part_numbers_and_category.add((model_id, number, category))

    return [
        model_id,
        manufacturer,
        machine_type,
        machine_model,
        list(part_numbers_and_category),
    ]


async def get_all_machine_models():
    """Returns an Async generator of machine models

    Returns:
        async-generator: ((manufacturer, machine_type, list(machine_models),...)
    """
    # Get Manufacturers
    logging.info("fetching manufacturers ...")
    manufacturers = await get_manufacturers()

    # Asynchronously get machine types
    logging.info("fetching machine types ...")
    machine_type_tasks = [(m, create_task(get_machine_types(m))) for m in manufacturers]

    for manufacturer, task in machine_type_tasks:
        machine_models = None
        machine_types = await task

        models_tasks = [
            (
                manufacturer,
                m_type,
                create_task(get_machine_models(manufacturer, m_type)),
            )
            for m_type in machine_types
        ]
        for manufacturer, m_type, m_task in models_tasks:
            m_models = await m_task
            machine_models = (manufacturer, m_type, m_models)

        yield machine_models


async def get_all_parts():
    """Returns an Async generator of function get_parts()'s return values

    Returns:
        async-generator[func]: (get_parts(), ...)
    """
    unique_model_id = 1
    async for model_list in get_all_machine_models():
        manufacturer, machine_type, machine_models = model_list
        logging.info(f"processing models for ({manufacturer}, {machine_type})...")
        tasks = []

        for m_model in machine_models:
            yield create_task(
                get_parts(unique_model_id, manufacturer, machine_type, m_model)
            )
            unique_model_id += 1
