import tkinter as tk
from tkinter import messagebox, filedialog
from python_hosts import Hosts, HostsEntry

IP_TYPE = "ipv4"
LOCALHOST = "127.0.0.1"
HOSTS_PATH = "C:/Windows/System32/drivers/etc/hosts"
XAMPP_VHOSTS_PATH = "C:/xampp/apache/conf/extra/httpd-vhosts.conf"


def clearInput():
    domainVal.set("")
    dirRootVal.set("")
    httpsVal.set(0)


def addCustomVHost():
    servername = domainVal.get()
    documentroot = dirRootVal.get()
    https = httpsVal.get()

    new_vhost = f"""
<VirtualHost *:80>
    ServerName {servername}

    DocumentRoot "{documentroot}"
    <Directory "{documentroot}">
        Options Indexes FollowSymLinks Includes ExecCGI
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
"""

    if https == 1:
        new_vhost += f"""
<VirtualHost *:443>
    ServerName {servername}

    DocumentRoot "{documentroot}"
    <Directory "{documentroot}">
        Options Indexes FollowSymLinks Includes ExecCGI
        AllowOverride All
        Require all granted
    </Directory>

    SSLEngine on
    SSLCertificateFile "C:/xampp/apache/conf/ssl.crt/server.crt"
    SSLCertificateKeyFile "C:/xampp/apache/conf/ssl.key/server.key"
</VirtualHost>
        """

    with open(XAMPP_VHOSTS_PATH, "a") as config:
        config.write(new_vhost)

    messagebox.showinfo(
        title="Success",
        message="Restart Apache first, then you can start developing."
    )


def addCustomHost():
    url = domainVal.get()
    hosts = Hosts(path=HOSTS_PATH)

    if hosts.exists(address=LOCALHOST, names=[url]):
        raise Exception('Host already exists.')

    new_host = HostsEntry(entry_type=IP_TYPE,
                          address=LOCALHOST, names=[url])
    hosts.add([new_host])
    hosts.write()


def handle():
    try:
        if not domainVal.get() or not dirRootVal.get():
            raise Exception("All fields are required.")

        addCustomHost()
        addCustomVHost()
        clearInput()
    except Exception as e:
        messagebox.showwarning(title="Error", message=str(e), parent=root)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("conf.ident")
    root.geometry()
    root.resizable(False, False)
    root.eval('tk::PlaceWindow . center')

    gridFrame = tk.Frame(root)
    gridFrame.pack(padx=5)

    domainVal = tk.StringVar()

    tk.Label(gridFrame, text="Domain").grid(row=0, column=0)

    urlEntry = tk.Entry(gridFrame, textvariable=domainVal, width=40)
    urlEntry.grid(row=0, column=1, columnspan=3)

    dirRootVal = tk.StringVar()

    dirRootEntry = tk.Entry(gridFrame, textvariable=dirRootVal, width=40)
    dirRootEntry.grid(row=1, column=1, columnspan=3)
    dirRootEntry.config(state=tk.DISABLED)

    tk.Button(
        gridFrame,
        text="Directory",
        command=lambda: dirRootVal.set(
            filedialog.askdirectory(
                title="Select the project entry point directory"
            )
        )
    ).grid(row=1, column=0)

    fieldset = tk.LabelFrame(root, text="Options")
    fieldset.pack(fill="both", expand=True, padx=10, pady=5)

    httpVal = tk.IntVar(value=1)
    httpsVal = tk.IntVar()

    httpCheckBtn = tk.Checkbutton(
        fieldset,
        text="Port 80 (http)",
        variable=httpVal
    )
    httpCheckBtn.grid(row=0, column=0)
    httpCheckBtn.config(state=tk.DISABLED)

    tk.Checkbutton(fieldset, text="Port 443 (https)",
                   variable=httpsVal).grid(row=0, column=1)

    tk.Button(root, text="Add To Host", command=handle).pack(fill="both")

    root.mainloop()
