from Connect import app, db

if __name__ == '__main__':
    # for i in dbx.files_list_folder("").entries:
    #     if os.path.exists("/app/Connect/static/img/uploads"+i.path_lower):
    #         _,f=dbx.files_download("/img1.png")
    #         print("success")

    #         f = f.content

    #         print(type(f))
    #         img = Image.open(io.BytesIO(f))
    #         img.save("/app/Connect/static/img/uploads"+i.path_lower)

        app.run(debug=True)

