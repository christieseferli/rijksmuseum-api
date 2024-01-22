import pytest
from .variables import (COLLECTION_URL,
                        ART_OBJECTS_ELEMENTS,
                        ART_OBJECTS_LINKS_ELEMENTS,
                        COUNT_FACETS_ELEMENTS,
                        IMAGE_ELEMENTS,
                        FACETS_FACETS_ELEMENTS,
                        FACETS_ELEMENTS)


@pytest.mark.parametrize('api_key, status_code', [
    ('0fiuZFh4', 200),
    ('', 401),
    (None, 401)
])
@pytest.mark.parametrize('culture_language', ['nl', 'en'])
def test_collection(session, culture_language, api_key, status_code):
    _session = session(culture=culture_language)
    items = {
        "involvedMaker": "Rembrandt van Rijn"
    }
    if api_key:
        items['key'] = api_key

    response_get = _session.get(COLLECTION_URL, params=items)
    assert response_get.status_code == status_code
    if response_get.status_code == 200:
        validate_response_get_from_collection(response_get.json())


@pytest.mark.parametrize('api_key, status_code', [
    ('0fiuZFh4', 200),
    ('', 401),
    (None, 401)
])
@pytest.mark.parametrize('culture_language', ['nl', 'en'])
@pytest.mark.parametrize(
    'object_number', ['SK-C-5',
                      # 'invalid_obj' 'TODO: clear error message to the user']
                      ])
def test_collection_by_object_number(
        session, culture_language, api_key, status_code, object_number):
    """ TODO: Validate this api response data """
    _session = session(culture=culture_language)
    items = {}
    if api_key:
        items['key'] = api_key

    collection_by_obj_number_url = f'{COLLECTION_URL}/{object_number}'
    response_get = _session.get(collection_by_obj_number_url, params=items)
    assert response_get.status_code == status_code


@pytest.mark.parametrize('api_key, status_code', [
    ('0fiuZFh4', 200),
    ('', 401),
    (None, 401)
])
@pytest.mark.parametrize('culture_language', ['nl', 'en'])
def test_collection_by_tiles(
        session, culture_language, api_key, status_code):
    """ TODO: Validate this api response data """
    _session = session(culture=culture_language)
    items = {}
    if api_key:
        items['key'] = api_key

    collection_by_tiles_url = f'{COLLECTION_URL}/SK-C-5/tiles'
    response_get = _session.get(collection_by_tiles_url, params=items)
    assert response_get.status_code == status_code, response_get.json()


def validate_response_get_from_collection(response_data):
    # 1. validate the presence of the expected elements
    # 2. validate the amount of elements of each available dictionary
    assert len(response_data) == 5, f'Missing element from {response_data}'
    assert response_data['elapsedMilliseconds'] == 0
    assert response_data['count'] > 0, 'Invalid "count" number'

    if response_data['countFacets']:
        assert len(response_data['countFacets']) == 2, \
            f"'Missing element from: {response_data['countFacets']}'"
        for count_facets_elements in COUNT_FACETS_ELEMENTS:
            assert response_data['countFacets'].get(count_facets_elements)
    if response_data['artObjects']:
        for data in response_data['artObjects']:
            assert len(data) == 12, f"Missing element from artObjects: {data}"
            for art_objects_element in ART_OBJECTS_ELEMENTS:
                assert data.get(art_objects_element)
            for art_objects_links_element in ART_OBJECTS_LINKS_ELEMENTS:
                assert len(data['links']) == 2, \
                    f"Missing element from artObjects Links: {data['links']}"
                assert data['links'].get(art_objects_links_element)
            if data['webImage']:
                assert len(data['webImage']) == 6, \
                    (f"Missing element from artObjects webImage:"
                     f"{data['webImage']}")
                for web_image_element in IMAGE_ELEMENTS:
                    assert data['webImage'].get(web_image_element)
            if data['headerImage']:
                assert len(data['headerImage']) == 6, \
                    (f"Missing element from artObjects headerImage:"
                     f"{data['headerImage']}")
                for header_image_element in IMAGE_ELEMENTS:
                    assert data['headerImage'].get(header_image_element)

    if response_data['facets']:
        for data in response_data['facets']:
            assert len(data) == 4, \
                f"Missing element from facets: {data}"
            assert len(data['facets']) <= 100
            for facets_elements in data['facets']:
                assert len(facets_elements) == 2, \
                    f"Missing element from facets: {data['facets']}"
                for facets_facets_elements in FACETS_FACETS_ELEMENTS:
                    assert facets_elements.get(facets_facets_elements)
            for facets_elements in FACETS_ELEMENTS:
                assert data.get(facets_elements)
