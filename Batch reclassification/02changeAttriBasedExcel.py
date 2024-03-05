import geopandas as gpd
import pandas as pd
import os
from pathlib import Path

#### 根据excel中的重分类体系，将shp属性重分类
#### Reclassify shp attributes based on the reclassification system in Excel
def reclassifyAttributes(excel_path, shp_path, old_field, new_field, output_shp_path):
    # 读取 Excel 文件
    # Read the Excel file
    df_excel = pd.read_excel(excel_path, usecols=[1, 2], names=[new_field, old_field], engine='openpyxl')
    cname_mapping = dict(zip(df_excel[old_field], df_excel[new_field]))

    # 读取 Shapefile 数据
    # Read the Shapefile data
    gdf = gpd.read_file(shp_path)

    # 新建 new_field 字段
    # Create a new_field column
    gdf[new_field] = ''

    # 遍历每个要素，根据 "CNAME" 取值赋值给 "type" 字段
    # Iterate through each feature, assign values to the "type" field based on "CNAME"
    for index, row in gdf.iterrows():
        cname_value = row[old_field]
        if cname_value in cname_mapping:
            gdf.at[index, new_field] = cname_mapping[cname_value]

    # 写入 Shapefile
    # Write to Shapefile
    gdf.to_file(output_shp_path, encoding='utf-8', force_utf8=True)

# ### 根据shp属性值，将每类数据导出为一个图层存储在新的文件夹
### Export each class of data as a separate layer based on shp attribute values
def ouptShpBasedAttributes(output_shp_path, output_folder, field_to_export):
    gdf = gpd.read_file(output_shp_path)
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # 根据 field_to_export 字段值将数据分组
    # Group the data based on the field_to_export column
    grouped_data = gdf.groupby(field_to_export)

    # 遍历每个组
    # Iterate through each group
    for group_name, group_data in grouped_data:
        # 创建文件夹
        # Create a folder
        group_folder = os.path.join(output_folder, str(group_name))
        Path(group_folder).mkdir(parents=True, exist_ok=True)

        # 保存 Shapefile 文件
        # Save Shapefile
        group_output_shp_path = os.path.join(group_folder, f'{group_name}.shp')
        group_data.to_file(group_output_shp_path, encoding='utf-8', force_utf8=True)

if __name__ == "__main__":
    #【功能1】： 根据excel中的重分类体系, 将shp属性重分类
    #【Feature 1】: Reclassify shp attributes based on the reclassification system in Excel
    excel_path = r'Reclassification File.xlsx'
    shp_path = r'shp\test.shp' 
    old_field = 'DLMC'
    new_field = 'type'
    output_shp_path = r'shp\test reclassified.shp'
    # 根据excel中的重分类体系, 将shp属性重分类
    # Reclassify shp attributes based on the reclassification system in Excel
    reclassifyAttributes(excel_path, shp_path, old_field, new_field, output_shp_path)
    
    # #【功能2】： 根据shp属性值，将每类数据导出为一个图层存储在新的文件夹
    # #【Feature 2】: Export each class of data as a separate layer based on shp attribute values
    # 读取修改后的 Shapefile
    # Read the modified Shapefile
    # output_shp_path = r'shp\test reclassified.shp' 
    # 确保输出文件夹存在
    # Ensure the output folder exists
    # output_folder = r'shp\分类型数据' 
    # field_to_export='type'
    # 根据shp属性值，将每类数据导出为一个图层存储在新的文件夹
    # Export each class of data as a separate layer based on shp attribute values
    # ouptShpBasedAttributes(output_shp_path, output_folder, field_to_export)  
