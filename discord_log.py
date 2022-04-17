import pickle
from gspread.cell import Cell

root_folder_id = '1psHvV-6_U8cgpsF1vlr322aXD9uRnDjp'


def append_to_dict_files(file, key, value):
    with open('./files/' + file + '/keys.txt', 'a') as f:
        f.write(str(key) + '\n')
    with open('./files/' + file + '/values.txt', 'a') as f:
        f.write(str(value) + '\n')

def read_list_file(file):
    out_dict = {}
    keys = []
    values = []
    with open('./files/' + file + '/keys.txt', 'r') as f:
        keys = f.readlines()
    with open('./files/' + file + '/values.txt', 'r') as f:
        values = f.readlines()

    for i in range(len(keys)):
        out_dict[keys[i]] = values[i]

    return out_dict

channel_dict = read_list_file('channel_dict')
server_dict = read_list_file('guild_dict')

def log(message, drive_client, sheets_client):
    channel_id = str(message.channel.id)
    channel_name = message.channel.name

    server_id = str(message.guild.id)
    server_name = message.guild.name

    message_id = str(message.id)
    text = message.content
    author_id = str(message.author.id)
    author = message.author

    # creating folders and sheets if they don't exist
    if channel_id not in channel_dict:
        if server_id not in server_dict.keys():
            body = {
                'name': server_name + ' (' + server_id + ')',
                'parents': [root_folder_id],
                'mimeType': 'application/vnd.google-apps.folder'
            }
            drive_folder_id = drive_client.files().create(body=body).execute()['id']
            server_dict[server_id] = drive_folder_id
            append_to_dict_files('guild_dict', server_id, drive_folder_id)
        body = {
            'name': channel_name + ' (' + channel_id + ')',
            'parents': [server_dict[server_id]],
            'mimeType': 'application/vnd.google-apps.spreadsheet'
        }
        sheet_id = drive_client.files().create(body=body).execute()['id']
        channel_dict[channel_id] = sheet_id
        append_to_dict_files('channel_dict', channel_id, sheet_id)
    sheet = sheets_client.open_by_key(channel_dict[channel_id]).sheet1
    row = len(sheet.get_all_values()) + 1

    cells = []
    cells.append(Cell(row=row, col=1, value=author))
    cells.append(Cell(row=row, col=2, value=text))
    cells.append(Cell(row=row, col=3, value='exists'))
    cells.append(Cell(row=row, col=4, value=message_id))
    sheet.update_cells(cells)



