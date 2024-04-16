# PointCloud_Tiling, GPL-3.0 license

""" 
Plot utility methods - Module (Python)

The module is adapted from:
https://github.com/Amsterdam-AI-Team/Urban_PointCloud_Processing
"""


import folium
import pandas as pd


from ..utils.las_utils import get_bbox_from_tile_code
from ..utils.rd_converter import RDWGS84Converter


def plot_tiles_map(tiles, train_tiles=[], width=1024, height=1024,    
                   zoom_control=True, zoom_start=14, opacity=0.25):
    """
    Visualise the locations of all point cloud tiles in a given folder and
    overlay them on an OpenStreetMap of the area. The returned map is
    interactive, i.e. it allows panning and zooming, and tilecodes are
    displayed as tooltip on hoovering.
    """
    tile_df = (pd.DataFrame(columns=['Tilecode', 'X1', 'Y1', 'Train'])
               .set_index('Tilecode'))
    for tilecode in tiles:
        ((x1, _), (_, y1)) = get_bbox_from_tile_code(tilecode)
        tile_df.loc[tilecode] = [x1, y1, False]
    for tilecode in train_tiles:
        tile_df.loc[tilecode, 'Train'] = True

    conv = RDWGS84Converter()

    center = conv.from_rd(int((tile_df.X1.max() + 50 + tile_df.X1.min()) / 2),
                          int((tile_df.Y1.max() + 50 + tile_df.Y1.min()) / 2))

    f = folium.Figure(width=width, height=height)

    # Create Folium background map.
    tiles_map = (folium.Map(location=center, tiles='cartodbpositron',
                            min_zoom=10, max_zoom=20, zoom_start=zoom_start,
                            zoom_control=zoom_control, control_scale=True)
                 .add_to(f))

    for index, row in tile_df.iterrows():
        rect = [conv.from_rd(row.X1, row.Y1),
                conv.from_rd(row.X1 + 50, row.Y1 + 50)]
        if row.Train:
            fc = 'darkorange'
            fop = opacity
        else:
            fc = 'royalblue'
            fop = 0.1
        (folium.Rectangle(bounds=rect, tooltip=index, color='royalblue',
                          weight=1, fill_color=fc, fill_opacity=fop)
         .add_to(tiles_map))

    return tiles_map