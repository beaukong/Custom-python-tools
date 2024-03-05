import geopandas as gpd
from shapely.geometry import LineString
import math as m

# Read the Shapefile of lines
# 读取线的Shapefile文件
file_path = r'DelStraightLine\data\Input.shp'#inputLineNODupli.shp'#
gdf = gpd.read_file(file_path)

# Create a temporary copy of the input layer
# 创建输入图层的临时副本
gdf_temp = gdf.copy()

# Define a function to check if a line is horizontal or vertical
# 定义一个函数来检查线是否是横平或竖直的
def is_horizontal_or_vertical(line):
    coords = line.coords
    # Check if there are two coordinates, and if the x or y coordinates are equal
    if len(coords) == 2 and (m.fabs(coords[0][0] - coords[1][0]) < 50 or m.fabs(coords[0][1] - coords[1][1]) < 50):
        # Check if removing this line would create a dangling end
        # If the number of adjacent lines to the start or end point of the line is 1, return False; otherwise, return True
        start_point, end_point = coords[0], coords[1]
        lines_after_removal = gdf_temp[~gdf_temp['geometry'].apply(lambda l: l == line)]

        # Get the number of lines connected to the start and end points
        start_point_connected = lines_after_removal['geometry'].apply(lambda l: l.coords[-1] == start_point or l.coords[0] == start_point)
        end_point_connected = lines_after_removal['geometry'].apply(lambda l: l.coords[-1] == end_point or l.coords[0] == end_point)

        # If the number of lines connected to the start or end point is 1, do not remove the line (avoid creating dangling ends)
        if sum(start_point_connected) == 1 or sum(end_point_connected) == 1:
            return False
        else:
            return True
    else:
        return False

# Iterate through each line in the input layer and check if it should be removed
# 逐条遍历输入图层的线，判断是否删除
for index, row in gdf_temp.iterrows():
    if is_horizontal_or_vertical(row['geometry']):
        gdf_temp = gdf_temp.drop(index)

# Save the temporary layer to a new Shapefile
# 保存临时图层到新的Shapefile文件
output_temp_path = r'DelStraightLine\data\Output2.shp'#inputLinesrRes.shp'#
gdf_temp.to_file(output_temp_path)
