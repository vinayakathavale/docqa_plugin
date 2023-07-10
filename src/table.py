import pandas as pd
import boto3


def run_textract_image(inp_file):
    client = boto3.client('textract', region_name='eu-west-1')

    response = client.analyze_document(Document={'Bytes': inp_file},
        FeatureTypes=["TABLES"])
    return response


def get_children_ids(block):
    for rels in block.get('Relationships', []):
        if rels['Type'] == 'CHILD':
            yield from rels['Ids']


def get_table_df_aws(response):

    blocks = response['Blocks']
    tables = map_blocks(blocks, 'TABLE')
    cells = map_blocks(blocks, 'CELL')
    words = map_blocks(blocks, 'WORD')
    selections = map_blocks(blocks, 'SELECTION_ELEMENT')

    dataframes = []

    for table in tables.values():

        # Determine all the cells that belong to this table
        table_cells = [cells[cell_id] for cell_id in get_children_ids(table)]

        # Determine the table's number of rows and columns
        n_rows = max(cell['RowIndex'] for cell in table_cells)
        n_cols = max(cell['ColumnIndex'] for cell in table_cells)
        content = [[None for _ in range(n_cols)] for _ in range(n_rows)]

        # Fill in each cell
        for cell in table_cells:
            cell_contents = [
                words[child_id]['Text']
                if child_id in words
                else selections[child_id]['SelectionStatus']
                for child_id in get_children_ids(cell)
            ]
            i = cell['RowIndex'] - 1
            j = cell['ColumnIndex'] - 1
            content[i][j] = ' '.join(cell_contents)

        # We assume that the first row corresponds to the column names
        dataframe = pd.DataFrame(content[1:], columns=content[0])
        dataframes.append(dataframe)

    return dataframes

def map_blocks(blocks, block_type):
    return {
        block['Id']: block
        for block in blocks
        if block['BlockType'] == block_type
    }