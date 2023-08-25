from datavision_beeyard_sdk.api.file import read_file
from datavision_beeyard_sdk.api.cell import read_cell
import json


def get_images(cell_id, client):
    """Get all images from a cell.

    This method will download all images present inside the BeeYard cell.

    Parameters
    ----------
    cell_id : str
        The BeeYard cell id where images are stored.
    client : AuthenticatedClient
        The BeeYard client used to connect to the platform.

    Returns
    -------
    list[bytes]
        The list of images. Each image is byte encoded.
        The list is empty if no image is present inside the cell.

    """
    cell_descriptor = read_cell.read(id=cell_id, client=client)
    files = [
        i.get("name")
        for i in cell_descriptor.get("files")
        if i.get("dataType") == "image"
    ]
    images = [
        read_file.read(id=cell_id, filename=file_name, client=client)
        for file_name in files
    ]
    return images


def get_annotations(overlays_json, annotation_type=None):
    """Get all annotations from an overlay.

    This methods get all annotations of a given type from a BeeYard cell.
    If the type is not specified, then all annotations will be returned.

    Parameters
    ----------
    overlays_json : json str
        A json string containing the overlay dictionary.
    annotation_type : str, optional
        The annotation type to retrive from the overlay, by default None.

    Returns
    -------
    list[dict]
        List of shapes. Each shape is a dictionary.

    Raises
    ------
    Exception
        If annotation type is not found in overlay.
    """
    overlays = json.loads(overlays_json)
    shapes = []
    if annotation_type is None:
        for overlay in overlays:
            for layer in overlay.get("overlay").get("layers"):
                for shape in layer.get("shapes"):
                    shapes.append(shape)
    else:
        for overlay in overlays:
            for layer in overlay.get("overlay").get("layers"):
                for shape in layer.get("shapes"):
                    if shape.get("typeName") == annotation_type:
                        shapes.append(shape)
        if len(shapes) == 0:
            raise Exception(f"Annotation type {annotation_type} not found in cell.")
    return shapes
