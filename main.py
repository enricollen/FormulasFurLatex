from cat.mad_hatter.decorators import tool, hook
from cat.log import log
from .image_parser import ImageParser

@hook
def rabbithole_instantiates_parsers(file_handlers: dict, cat) -> dict:
    """
    Modifies the file handler dictionary to use ImageParser for specific image types.
    Args:
        file_handlers (dict): Existing file handlers.
        cat: instance of the cat.

    Returns:
        dict: Updated file handlers with ImageParser instances.
    """

    supported_formats = ["image/png", "image/jpeg", "image/webp"]
    for format in supported_formats:
        file_handlers[format] = ImageParser()

    return file_handlers

@hook
def before_rabbithole_splits_text(text: list, cat):
    """
    Process text before splitting by checking source metadata and updating the user about the process.
    Args:
        text (list): List of Document objects.
        cat: instance of the cat.

    Returns:
        list: The same or modified text list after processing.
    """
    try:
        first_document = text[0]
        if first_document.metadata.get("source") == "Cat_Latex":
            cat.send_ws_message(content="Reading image...", msg_type="chat")
            content = first_document.page_content
            name = first_document.metadata.get("name", "")

            message = f"<p>The formula detected in the image <b>{name}</b> is: \n</p>{content}"
            cat.send_ws_message(content=message, msg_type="chat")

    except IndexError:
        log.error("Received empty text list for processing.")
    except KeyError as e:
        log.error(f"Metadata key missing: {e}")

    return text