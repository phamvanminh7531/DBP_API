from flask import Flask, request, jsonify
from smb.SMBConnection import SMBConnection

app = Flask(__name__)

@app.route('/smb-files', methods=['GET'])
def get_smb_files():
    # Kết nối đến SMB server
    conn = SMBConnection('ngoc.ho', 'Kiemthan@123', 'DESKTOP-C9K8OPC', 'SERVER', use_ntlm_v2=True)
    conn.connect('192.168.1.254', 139)

    # Lấy đường dẫn từ query parameter
    path = request.args.get('path', '/DBplus')

    try:
        shares = conn.listPath('shared_folder', path)
        items = [
            {"name": file.filename, "isDirectory": file.isDirectory}
            for file in shares
            if file.filename not in ['.', '..']
        ]
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

    return jsonify(items)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
