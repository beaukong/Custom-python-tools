import geopandas as gpd
import pandas as pd
import os

###导出文件夹下多个shp数据某字段的唯一值
###Export the unique value of a field of multiple shp data in the export folder
def outputUniqueAttributeFromFolder(folder_path, excel_path, field_to_export):
    # 存储唯一值的列表
    # List to store unique values
    unique_values = []

    # 遍历文件夹中的每个 shp 文件
    # Iterate through each shp file in the folder
    for filename in os.listdir(folder_path):
        print(filename)
        if filename.endswith('.shp'):
            file_path = os.path.join(folder_path, filename)
            # 读取 shapefile 文件
            # Read the shapefile
            gdf = gpd.read_file(file_path)
            # 获取唯一值
            # Get unique values
            unique_values.extend(gdf[field_to_export].unique())

    # 去除重复的唯一值
    # Remove duplicate unique values
    unique_values = list(set(unique_values))

    # 创建一个 DataFrame
    # Create a DataFrame
    df = pd.DataFrame({field_to_export: unique_values})

    # 导出到 Excel 文件
    # Export to Excel file
    df.to_excel(excel_path, index=False)

###导出单个shp数据某字段的唯一值
###Export the unique value of a field of a single shp data
def outputUniqueAttribute(shp_path, excel_path, field_to_export):
    gdf = gpd.read_file(shp_path)

    # 获取唯一值
    # Get unique values
    unique_values = gdf[field_to_export].unique()

    # 创建一个 DataFrame
    # Create a DataFrame
    df = pd.DataFrame({field_to_export: unique_values})

    # 导出到 Excel 文件
    # Export to Excel file
    df.to_excel(excel_path, index=False)

###导出单个shp数据某字段的所有值
###Export all values of a field of a single shp data
def outputAttribute(shp_path, excel_path, field_to_export):
    gdf = gpd.read_file(shp_path)

    # 提取字段属性
    # Extract field attributes
    field_data = gdf[field_to_export]
    # 将数据保存到 Excel 文件
    # Save data to Excel file
    field_data.to_excel(excel_path, index=False, header=[field_to_export])

# __main()__:
if __name__ == "__main__":
    ###导出 shp数据中某字段的唯一值 
    ###Export the unique value of a field in the shp data
    # 指定要导出的字段
    # Specify the field to export
    field_to_export = 'DLMC'
    # 读取 shapefile 文件
    # Read the shapefile
    shp_path = r'shp\test.shp'
    excel_path = r'Reclassification File.xlsx'
    #folder_path=r'独立图层'    
    outputUniqueAttribute(shp_path, excel_path, field_to_export)
