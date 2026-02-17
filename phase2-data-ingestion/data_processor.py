# import logging
#
# def setup_logging(level: str):
#     numeric_level = getattr(logging, level.upper(), logging.INFO)
#
#     logging.basicConfig(
#         level=numeric_level,
#         format="%(asctime)s [%(levelname)s] %(message)s",
#         handlers=[
#             logging.StreamHandler(),  # console
#             logging.FileHandler("etl.log"),  # file output
#         ],
#     )


