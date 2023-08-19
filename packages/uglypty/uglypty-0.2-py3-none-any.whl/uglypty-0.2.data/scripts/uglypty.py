import copy
from PyQt6 import QtCore, QtGui, QtWidgets
from Library.qtssh_widget import Ui_Terminal as qtssh_widget
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QTreeWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QProcess
import yaml
import socket
import sqlite3
from Library.creds_widget import CredentialsManagerWidget
from Library.util import cryptonomicon, generate_key, create_db
from log_viewer2 import FileViewer

welcome_html = '''
<style>
  body {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }

  .container {
    text-align: center;
  }

  h1 {
    color: #FF9800;

  }

  p {
    color: #607D8B;
    text-align: left;
  }

  ul {
    color: #4CAF50;
    text-align: left;
    list-style-position: inside;
    padding-left: 0;
  }

  li {
    color: #2196F3;
  }
</style>

<body>
  <div class="container">
    <h1>UglyPTY&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</h1>
    <p>
      <b>UglyPTY</b> is a <span style="color: #FF9800;">PyQt6-based</span> application that provides a user interface for interacting with terminals and managing sessions. It offers the following features:
    </p>
    <ul>
    <li>
        <b><span style="color: #FF9800;">Tabbed Terminals</span></b>: UglyPTY provides a tabbed interface for managing multiple terminals simultaneously. You can open and close tabs as needed.
      </li>
      <li>
        Dark/Light Theme: UglyPTY provides both Dark and Light view options.
      </li>
      <li>
        Tree View: UglyPTY includes a tree view on the left-hand side, allowing you to navigate and select different terminals or sessions.
      </li>
      <li>
        Context Menu: Right-clicking on the tree view opens a context menu with options like connecting to a terminal or displaying properties.
      </li>

      <li>
        Menus: The application includes a menu bar with various options, such as opening inventory files, managing credentials, and adjusting the view mode (light or dark).
      </li>
      <li>
        Help: UglyPTY offers a help menu with information about the application and its usage.
      </li>
    </ul>
    <p>
      UglyPTY is designed to provide a user-friendly experience for working with terminals and managing sessions efficiently.
    </p>
  </div>
</body>

'''


class Ui_dlgSelectCreds(QtWidgets.QDialog):
    def __init__(self, creds, selected_item, *args, **kwargs):
        super(Ui_dlgSelectCreds, self).__init__(*args, **kwargs)
        self.setWindowTitle("Select Credentials")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.comboCreds = QtWidgets.QComboBox(self)
        self.comboCreds.addItem("-- creds --", 0)

        for displayname, id in creds:
            self.comboCreds.addItem(displayname, id)

        self.verticalLayout.addWidget(self.comboCreds)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)  # Add this line
        self.verticalLayout.addWidget(self.buttonBox)

    def closeEvent(self, event):
        self.buttonBox.rejected.emit()  # Emit the rejected signal

    def get_selected_cred(self):
        return self.comboCreds.currentData()

class AddSessionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add SSH Session")

        # Create layout and form
        self.layout = QtWidgets.QFormLayout(self)

        # Existing fields
        self.displayNameLineEdit = QtWidgets.QLineEdit(self)
        self.hostLineEdit = QtWidgets.QLineEdit(self)
        self.hostPortEdit = QtWidgets.QLineEdit(self)
        self.hostPortEdit.setText('22')
        self.credsidLineEdit = QtWidgets.QLineEdit(self)

        # New fields for the extended schema
        self.deviceTypeLineEdit = QtWidgets.QLineEdit(self)
        self.modelLineEdit = QtWidgets.QLineEdit(self)
        self.serialNumberLineEdit = QtWidgets.QLineEdit(self)
        self.softwareVersionLineEdit = QtWidgets.QLineEdit(self)
        self.vendorLineEdit = QtWidgets.QLineEdit(self)

        # Add rows
        self.layout.addRow("Display Name", self.displayNameLineEdit)
        self.layout.addRow("Host or IP", self.hostLineEdit)
        self.layout.addRow("Host Port", self.hostPortEdit)
        self.layout.addRow("Credsid", self.credsidLineEdit)
        self.layout.addRow("Device Type", self.deviceTypeLineEdit)
        self.layout.addRow("Model", self.modelLineEdit)
        self.layout.addRow("Serial Number", self.serialNumberLineEdit)
        self.layout.addRow("Software Version", self.softwareVersionLineEdit)
        self.layout.addRow("Vendor", self.vendorLineEdit)

        # Buttons
        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel, self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addRow(self.buttonBox)



class EditSessionDialog(QtWidgets.QDialog):
    def __init__(self, session_item, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit SSH Session")
        self.session_item = session_item  # The tree item representing the session

        # Create layout and form
        self.layout = QtWidgets.QFormLayout(self)

        # Existing fields
        self.displayNameLineEdit = QtWidgets.QLineEdit(self)
        self.displayNameLineEdit.setText(self.session_item.refBinding['display_name'])

        self.hostLineEdit = QtWidgets.QLineEdit(self)
        self.hostLineEdit.setText(self.session_item.refBinding['host'])

        self.hostPortEdit = QtWidgets.QLineEdit(self)
        self.hostPortEdit.setText(self.session_item.refBinding.get('port', '22'))

        self.credsidLineEdit = QtWidgets.QLineEdit(self)
        self.credsidLineEdit.setText(str(self.session_item.refBinding['credsid']))

        # New fields for the extended schema
        self.deviceTypeLineEdit = QtWidgets.QLineEdit(self)
        self.deviceTypeLineEdit.setText(self.session_item.refBinding.get('DeviceType', ''))

        self.modelLineEdit = QtWidgets.QLineEdit(self)
        self.modelLineEdit.setText(self.session_item.refBinding.get('Model', ''))

        self.serialNumberLineEdit = QtWidgets.QLineEdit(self)
        self.serialNumberLineEdit.setText(self.session_item.refBinding.get('SerialNumber', ''))

        self.softwareVersionLineEdit = QtWidgets.QLineEdit(self)
        self.softwareVersionLineEdit.setText(self.session_item.refBinding.get('SoftwareVersion', ''))

        self.vendorLineEdit = QtWidgets.QLineEdit(self)
        self.vendorLineEdit.setText(self.session_item.refBinding.get('Vendor', ''))

        # Add rows
        self.layout.addRow("Display Name", self.displayNameLineEdit)
        self.layout.addRow("Host", self.hostLineEdit)
        self.layout.addRow("Port", self.hostPortEdit)
        self.layout.addRow("Credsid", self.credsidLineEdit)
        self.layout.addRow("Device Type", self.deviceTypeLineEdit)
        self.layout.addRow("Model", self.modelLineEdit)
        self.layout.addRow("Serial Number", self.serialNumberLineEdit)
        self.layout.addRow("Software Version", self.softwareVersionLineEdit)
        self.layout.addRow("Vendor", self.vendorLineEdit)

        # Buttons
        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel, self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addRow(self.buttonBox)

class SearchDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search SSH Sessions")

        # Create layout and form
        self.layout = QtWidgets.QVBoxLayout(self)

        self.searchLineEdit = QtWidgets.QLineEdit(self)
        self.searchButton = QtWidgets.QPushButton("Search", self)
        self.resultListWidget = QtWidgets.QListWidget(self)
        self.connectButton = QtWidgets.QPushButton("Connect", self)

        # Add widgets to layout
        self.layout.addWidget(self.searchLineEdit)
        self.layout.addWidget(self.searchButton)
        self.layout.addWidget(self.resultListWidget)
        self.layout.addWidget(self.connectButton)

        # Connect signals
        self.searchButton.clicked.connect(self.search)
        self.connectButton.clicked.connect(self.connect)

    def search(self):
        # Clear the list widget
        self.resultListWidget.clear()

        # Get the search string
        search_string = self.searchLineEdit.text().lower()

        # Traverse the tree and search for sessions
        root = self.parent().treeWidget.invisibleRootItem()
        folder_count = root.childCount()

        for i in range(folder_count):
            try:
                folder_item = root.child(i)
                session_count = folder_item.childCount()

                for j in range(session_count):

                    try:
                        session_item = folder_item.child(j)
                        display_name = session_item.refBinding['display_name'].lower()
                        host = session_item.refBinding['host'].lower()
                        if search_string in display_name or search_string in host:
                            # Add the session item to the list widget
                            print(f"Found")
                            try:
                                list_item = QtWidgets.QListWidgetItem(f"{display_name} ({host})")
                                list_item.setData(QtCore.Qt.ItemDataRole.UserRole, session_item)
                                self.resultListWidget.addItem(list_item)
                            except Exception as e:
                                print(f"error loading list item: {e}")
                    except Exception as e:
                        print(f"Searching tree error: {e}")
            except Exception as e:
                print(f"Folder search error: {e}")

    def connect(self):
        # Get the selected item
        list_item = self.resultListWidget.currentItem()

        # Check if an item is selected
        if list_item is not None:
            # Get the session item
            session_item = list_item.data(QtCore.Qt.ItemDataRole.UserRole)

            creds = self.parent().get_all_creds()
            # Show the dialog
            dlgSelectCreds = Ui_dlgSelectCreds(creds, session_item)
            dlgSelectCreds.exec()

            # Get selected id
            selected_id = dlgSelectCreds.get_selected_cred()
            if selected_id == 0:
                return
            # Use the id here
            print(f"Selected ID: {selected_id}")

            use_creds = self.parent().get_one_creds(selected_id)
            username = use_creds[0]
            encrypted_password = use_creds[1]
            unencrypted_password = cryptonomicon(encrypted_password)

            print(f"Properties: {session_item.refBinding}")
            host = str(session_item.refBinding['host'])
            if not self.parent().is_ssh_open(host, session_item.refBinding.get('port', '22'), 5):
                self.parent().notify("Connection Failure", f"Unable to quick connect on port {session_item.refBinding.get('port', '22')}")
                return

            hostinfo = {
                "host": session_item.refBinding['host'],
                "port": session_item.refBinding.get('port', '22'),
                "username": username,
                "password": unencrypted_password,
                "log_filename": f"./logs/session_{session_item.refBinding['host']}.log",
                "theme": self.parent().theme
            }

            try:
                self.parent().stackedWidget.setCurrentIndex(1)
                ssh_widget = qtssh_widget((hostinfo, self.parent()))
                ssh_widget.setObjectName("ssh_widget")

                layout = QtWidgets.QVBoxLayout()
                layout.addWidget(ssh_widget)

                # Create new tab and add SSH widget
                new_tab = QtWidgets.QWidget()
                new_tab.setLayout(layout)

                ssh_widget.setVisible(True)
                # Add the new tab and set its title to the host
                index = self.parent().twTerminals.addTab(new_tab, hostinfo['host'])

                # Set the new tab as the current tab
                self.parent().twTerminals.setCurrentIndex(index)
            except:
                pass


class UtlyPty(QtWidgets.QWidget):
    def setupUi(self, Ui_UglyPTY):
        Ui_UglyPTY.setObjectName("Ui_UglyPTY")
        Ui_UglyPTY.resize(1291, 775)
        self.current_file = None
        self.logview = None
        self.ace_window = None
        self.terminals = None
        self.theme = global_theme
        self.cut_item = None
        self.copy_item = None
        self.centralwidget = QtWidgets.QWidget(parent=Ui_UglyPTY)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(parent=self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter.setObjectName("splitter")
        self.widget = QtWidgets.QWidget(parent=self.splitter)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter_2 = QtWidgets.QSplitter(parent=self.widget)
        self.splitter_2.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter_2.setHandleWidth(1)
        self.splitter_2.setObjectName("splitter_2")
        self.widget_2 = QtWidgets.QWidget(parent=self.splitter_2)
        self.widget_2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setContentsMargins(0, 8, 0, 8)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.treeWidget = QtWidgets.QTreeWidget(parent=self.widget_2)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.verticalLayout_3.addWidget(self.treeWidget)

        # Create a QMenu object for the context menu
        self.context_menu = QMenu(self)

        # Add actions to the context menu
        self.action_connect = QAction("Connect...", self)
        self.context_menu.addAction(self.action_connect)

        self.action_display_properties = QAction("Display Properties...", self)
        self.context_menu.addAction(self.action_display_properties)

        self.action_cut = QAction("Cut", self)
        self.action_cut.triggered.connect(self.cut_session)
        self.context_menu.addAction(self.action_cut)  # Add the cut action

        self.action_paste = QAction("Paste Cut", self)
        self.action_paste.triggered.connect(self.paste_session)
        self.addAction(self.action_paste)

        self.action_copy = QAction("Copy", self)
        self.action_copy.triggered.connect(self.copy_session)
        self.context_menu.addAction(self.action_copy)

        self.action_paste_copy = QAction("Paste Copy", self)
        self.action_paste_copy.triggered.connect(self.paste_copied_session)

        # Connect actions to slots (functions)
        self.action_connect.triggered.connect(self.on_action_connect)
        self.action_display_properties.triggered.connect(self.on_action_display_properties)

        # Connect the context menu to the tree widget
        self.treeWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.open_menu)

        self.widget_3 = QtWidgets.QWidget(parent=self.splitter_2)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.widget_3)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.textBrowser = QtWidgets.QTextBrowser(parent=self.page)
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setHtml(welcome_html)
        self.verticalLayout_5.addWidget(self.textBrowser)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.twTerminals = QtWidgets.QTabWidget(parent=self.page_2)
        self.twTerminals.setObjectName("twTerminals")
        # Enable the close button on the tab
        self.twTerminals.setTabsClosable(True)
        # Connect the tabCloseRequested signal to a slot method
        self.twTerminals.tabCloseRequested.connect(self.close_tab)
        self.verticalLayout_6.addWidget(self.twTerminals)
        self.stackedWidget.addWidget(self.page_2)
        self.verticalLayout_4.addWidget(self.stackedWidget)
        self.verticalLayout_2.addWidget(self.splitter_2)
        self.wgtFp = QtWidgets.QWidget(parent=self.splitter)
        self.wgtFp.setMaximumSize(QtCore.QSize(16777215, 50))
        self.wgtFp.setObjectName("wgtFp")
        self.wgtFp.setVisible(False)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.wgtFp)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblInventory = QtWidgets.QLabel(parent=self.wgtFp)
        self.lblInventory.setObjectName("lblInventory")
        self.horizontalLayout.addWidget(self.lblInventory)
        self.verticalLayout.addWidget(self.splitter)
        Ui_UglyPTY.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=Ui_UglyPTY)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1291, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuCreds")
        self.menuOptions = QtWidgets.QMenu(parent=self.menubar)
        self.menuOptions.setObjectName("menuOptions")

        self.menuHelp = QtWidgets.QMenu(parent=self.menubar)
        self.menuHelp.setObjectName("menuHelp")

        # create the actions
        self.actionLogViewer = QtGui.QAction(self)
        self.actionLogViewer.setText("Log Viewer")
        self.actionLogViewer.triggered.connect(self.on_actionLogViewer_triggered)

        # add the actions to the tools menu
        self.menuOptions.addAction(self.actionLogViewer)

        Ui_UglyPTY.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=Ui_UglyPTY)
        self.statusbar.setObjectName("statusbar")
        Ui_UglyPTY.setStatusBar(self.statusbar)
        self.actionOpen_Inventory_File = QtGui.QAction(parent=Ui_UglyPTY)
        self.actionOpen_Inventory_File.setObjectName("actionOpen_Inventory_File")

        # Create the "File" menu and the "New Folder" action
        self.actionNewFolder = QtGui.QAction("New Folder", self)

        # Add the "New Folder" action to the "File" menu
        self.menuFile.addAction(self.actionNewFolder)

        # Connect the "New Folder" action to the new_folder method
        self.actionNewFolder.triggered.connect(self.new_folder)

        self.actionExit = QtGui.QAction(parent=Ui_UglyPTY)
        self.actionExit.setObjectName("actionExit")
        self.actionCredentials = QtGui.QAction(parent=Ui_UglyPTY)
        self.actionCredentials.setObjectName("actionCredentials")
        self.actionAbout = QtGui.QAction(parent=Ui_UglyPTY)
        self.actionAbout.setObjectName("actionAbout")

        self.actionNew_Session = QtGui.QAction(parent=Ui_UglyPTY)
        self.actionNew_Session.setObjectName("actionNew_Session")
        self.menuFile.addAction(self.actionNew_Session)
        self.menuFile.addAction(self.actionOpen_Inventory_File)
        # self.menuFile.addAction(self.actionImportInventory)

        self.actionOpen_Inventory_File.triggered.connect(lambda: self.open_inventory_file(None))
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuOptions.addAction(self.actionCredentials)

        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.actionLight = QtGui.QAction(parent=Ui_UglyPTY)
        self.actionLight.setObjectName("actionLight")
        self.actionLightDark = QtGui.QAction(parent=Ui_UglyPTY)
        self.actionLightDark.setObjectName("actionLight")
        self.actionDark = QtGui.QAction(parent=Ui_UglyPTY)
        self.actionDark.setObjectName("actionDark")
        self.actionDarkLight = QtGui.QAction(parent=Ui_UglyPTY)
        self.actionDarkLight.setObjectName("actionDark")

        self.menuMode = QtWidgets.QMenu(parent=self.menuOptions)
        self.menuMode.setObjectName("menuMode")
        self.menuMode.addAction(self.actionLight)
        self.menuMode.addAction(self.actionLightDark)
        self.menuMode.addAction(self.actionDark)
        self.menuMode.addAction(self.actionDarkLight)

        self.menuOptions.addMenu(self.menuMode)

        self.retranslateUi(Ui_UglyPTY)
        self.stackedWidget.setCurrentIndex(0)
        self.twTerminals.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Ui_UglyPTY)

        self.actionNew_Session.triggered.connect(self.new_session)

        # load default inventory
        self.open_inventory_file("./sessions/sessions.yaml")
        self.current_file = "./sessions/sessions.yaml"
        # self.open_inventory_file("./sessions/example.yaml")

        # Create the context menus for session nodes and folder nodes
        self.folderContextMenu = QtWidgets.QMenu(self.treeWidget)

        # Add actions to the session context menu
        self.actionEditSession = QtGui.QAction("Edit", self.context_menu)
        self.actionDeleteSession = QtGui.QAction("Delete", self.context_menu)
        self.context_menu.addAction(self.actionEditSession)
        self.context_menu.addAction(self.actionDeleteSession)

        # Add actions to the folder context menu
        self.actionAddSession = QtGui.QAction("Add Session", self.folderContextMenu)
        self.actionRenameFolder = QtGui.QAction("Rename Folder", self.folderContextMenu)
        self.actionDeleteFolder = QtGui.QAction("Delete Folder", self.folderContextMenu)
        self.folderContextMenu.addAction(self.actionAddSession)
        self.folderContextMenu.addAction(self.actionRenameFolder)
        self.folderContextMenu.addAction(self.actionDeleteFolder)
        self.folderContextMenu.addAction(self.action_paste_copy)
        self.folderContextMenu.addAction(self.action_paste)
        # Connect the context menu actions to the appropriate methods
        self.actionEditSession.triggered.connect(self.edit_session)
        self.actionDeleteSession.triggered.connect(self.delete_session)
        self.actionAddSession.triggered.connect(self.add_session)
        self.actionRenameFolder.triggered.connect(self.rename_folder)
        self.actionDeleteFolder.triggered.connect(self.delete_folder)
        # Connect the customContextMenuRequested signal of the tree widget to the show_context_menu method
        # Create the context menu for the root
        self.rootContextMenu = QtWidgets.QMenu(self.treeWidget)

        # Add the "New Folder" action to the root context menu
        self.actionNewFolder = QtGui.QAction("New Folder", self.rootContextMenu)
        self.rootContextMenu.addAction(self.actionNewFolder)

        # Connect the "New Folder" action to the new_folder method
        self.actionNewFolder.triggered.connect(self.new_folder)

        self.treeWidget.customContextMenuRequested.connect(self.show_context_menu)

    def retranslateUi(self, Ui_UglyPTY):
        _translate = QtCore.QCoreApplication.translate
        Ui_UglyPTY.setWindowTitle(_translate("Ui_UglyPTY", "UglyPTY"))
        self.lblInventory.setText(_translate("Ui_UglyPTY", "Inventory"))
        self.menuFile.setTitle(_translate("Ui_UglyPTY", "File"))
        self.menuOptions.setTitle(_translate("Ui_UglyPTY", "Options"))
        # self.menuTools.setTitle(_translate("Ui_UglyPTY", "Tools"))
        self.menuHelp.setTitle(_translate("Ui_UglyPTY", "Help"))
        self.actionOpen_Inventory_File.setText(_translate("Ui_UglyPTY", "Open Inventory File"))
        self.actionExit.setText(_translate("Ui_UglyPTY", "Exit"))
        self.actionCredentials.setText(_translate("Ui_UglyPTY", "Credentials"))
        self.actionAbout.setText(_translate("Ui_UglyPTY", "About"))
        self.actionNew_Session.setText(_translate("Ui_UglyPTY", "New Session"))
        # self.menuView.setTitle(_translate("Ui_UglyPTY", "View"))
        self.menuMode.setTitle(_translate("Ui_UglyPTY", "Theme"))
        self.actionLight.setText(_translate("Ui_UglyPTY", "Light"))
        self.actionLightDark.setText(_translate("Ui_UglyPTY", "Light on Dark"))
        self.actionDarkLight.setText(_translate("Ui_UglyPTY", "Dark on Light"))
        self.actionDark.setText(_translate("Ui_UglyPTY", "Dark"))

        self.actionLight.triggered.connect(self.light_mode)
        self.actionLightDark.triggered.connect(self.light_dark_mode)
        self.actionDark.triggered.connect(self.dark_mode)
        self.actionDarkLight.triggered.connect(self.dark_light_mode)
        self.actionCredentials.triggered.connect(self.credentials_option_triggered)
        self.actionExit.triggered.connect(lambda: sys.exit(0))


    def copy_session(self):
        QtCore.QTimer.singleShot(50, self._copy_session)

    def _copy_session(self):
        self.context_menu.close()
        self.copy_item = self.treeWidget.currentItem()
        self.context_menu.close()
        self.save_tree_to_file()

    def paste_copied_session(self):
        QtCore.QTimer.singleShot(50, self._paste_copied_session)

    def _paste_copied_session(self):
        if self.copy_item is not None:
            # Create a new QTreeWidgetItem
            copied_session = QtWidgets.QTreeWidgetItem()

            # Copy over the properties from the source item
            for i in range(self.copy_item.columnCount()):
                copied_session.setText(i, self.copy_item.text(i))
            copied_session.refBinding = copy.deepcopy(self.copy_item.refBinding)

            # Add the new item to the current folder
            self.treeWidget.currentItem().addChild(copied_session)
            self.context_menu.close()
            self.save_tree_to_file()

    # _paste_copied_session

    def cut_session(self):
        QtCore.QTimer.singleShot(50, self._cut_session)

    def _cut_session(self):
        current_item = self.treeWidget.currentItem()
        # Check if the current item is a session (has a parent)
        if current_item is not None and current_item.parent() is not None:
            self.cut_item = current_item
            # Remove the session from its current folder
            current_item.parent().removeChild(current_item)
            self.context_menu.close()
            self.save_tree_to_file()

    def paste_session(self):
        QtCore.QTimer.singleShot(50, self._paste_session)

    def _paste_session(self):
        current_item = self.treeWidget.currentItem()
        # Check if there is a session to paste and if the current item is a folder (does not have a parent)
        if self.cut_item is not None and current_item is not None and current_item.parent() is None:
            # Add the cut session to the current folder
            current_item.addChild(self.cut_item)
            # Clear the cut session
            self.cut_item = None
            self.save_tree_to_file()
            self.context_menu.close()

    # stub functions
    def on_actionLogViewer_triggered(self):
        # TODO: Implement the function
        self.logview = FileViewer()
        self.logview.show()
        # logview.exec()

    def search(self):
        dialog = SearchDialog(self)
        dialog.exec()

    def add_session(self):
        # Get the current item
        current_item = self.treeWidget.currentItem()

        # Check if an item is selected and it is a folder
        if current_item is not None and current_item.parent() is None:
            dialog = AddSessionDialog()
            result = dialog.exec()

            if result == QtWidgets.QDialog.DialogCode.Accepted:
                # Create the session item
                session_item = QtWidgets.QTreeWidgetItem(current_item)
                session_item.setText(0, dialog.displayNameLineEdit.text())

                # Extract data with the new schema fields
                session_item.refBinding = {
                    'display_name': dialog.displayNameLineEdit.text(),
                    'host': dialog.hostLineEdit.text(),
                    'port': dialog.hostPortEdit.text(),
                    'credsid': int(dialog.credsidLineEdit.text()),
                    'DeviceType': dialog.deviceTypeLineEdit.text(),
                    'Model': dialog.modelLineEdit.text(),
                    'SerialNumber': dialog.serialNumberLineEdit.text(),
                    'SoftwareVersion': dialog.softwareVersionLineEdit.text(),
                    'Vendor': dialog.vendorLineEdit.text()
                }

                # Save changes to the YAML file
                self.save_tree_to_file()
                self.context_menu.close()


    def rename_folder(self):
        # Get the current item
        current_item = self.treeWidget.currentItem()

        # Check if an item is selected and it is a folder
        if current_item is not None and current_item.parent() is None:
            # Ask for the new name
            new_name, ok = QtWidgets.QInputDialog.getText(self, 'Rename Folder', 'Enter the new name of the folder:',
                                                          text=current_item.text(0))

            if ok and new_name:
                # Set the new name of the folder
                current_item.setText(0, new_name)

                # Save changes to the YAML file
                self.save_tree_to_file()
                self.context_menu.close()

    def delete_session(self):
        QtCore.QTimer.singleShot(50, self._delete_session)

    def _delete_session(self):
        # Get the current item
        current_item = self.treeWidget.currentItem()

        # Check if an item is selected and it is a session
        if current_item is not None and current_item.parent() is not None:
            # Ask for confirmation
            reply = QtWidgets.QMessageBox.question(
                self, 'Delete Session',
                f"Are you sure you want to delete the session '{current_item.text(0)}'?",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                QtWidgets.QMessageBox.StandardButton.No
            )

            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                # Remove the session item
                current_item.parent().removeChild(current_item)
                self.save_tree_to_file()
                self.context_menu.close()

    def delete_folder(self):
        # Get the current item
        current_item = self.treeWidget.currentItem()

        # Check if an item is selected and it is a folder
        if current_item is not None and current_item.parent() is None:
            # Ask for confirmation
            reply = QtWidgets.QMessageBox.question(
                self, 'Delete Folder',
                f"Are you sure you want to delete the folder '{current_item.text(0)}' and all its sessions?",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                QtWidgets.QMessageBox.StandardButton.No
            )

            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                # Remove the folder item
                self.treeWidget.invisibleRootItem().removeChild(current_item)
                self.save_tree_to_file()
            self.context_menu.close()

    def edit_session(self):
        current_selected = self.treeWidget.currentItem()
        if current_selected is not None and current_selected.parent() is not None:  # if the item has a parent, it's a session
            dialog = EditSessionDialog(current_selected)
            result = dialog.exec()

            if result == QtWidgets.QDialog.DialogCode.Accepted:
                # Update the refBinding property with the new schema fields
                current_selected.refBinding = {
                    'display_name': dialog.displayNameLineEdit.text(),
                    'host': dialog.hostLineEdit.text(),
                    'port': dialog.hostPortEdit.text(),
                    'credsid': dialog.credsidLineEdit.text(),  # Save credsID as a string
                    'DeviceType': dialog.deviceTypeLineEdit.text(),
                    'Model': dialog.modelLineEdit.text(),
                    'SerialNumber': dialog.serialNumberLineEdit.text(),
                    'SoftwareVersion': dialog.softwareVersionLineEdit.text(),
                    'Vendor': dialog.vendorLineEdit.text()
                }

                # Reflect changes in the tree widget
                current_selected.setText(0, dialog.displayNameLineEdit.text())

                # Save changes to the YAML file
                self.save_tree_to_file()

            self.context_menu.close()

    def show_context_menu(self, position):
        item = self.treeWidget.itemAt(position)
        if item is not None:
            if item.parent() is not None:
                # If the item has a parent, it's a session
                self.action_cut.setVisible(True)  # Show the cut action
                self.action_copy.setVisible(True)  # Show the copy action
                self.context_menu.exec(self.treeWidget.viewport().mapToGlobal(position))
            else:
                # If the item does not have a parent, it's a folder
                self.action_cut.setVisible(False)  # Hide the cut action
                self.action_copy.setVisible(False)  # Hide the copy action
                self.action_paste.setVisible(
                    self.cut_item is not None if self.cut_item else False)  # Show or hide the paste action
                self.action_paste_copy.setVisible(
                    self.copy_item is not None if self.copy_item else False)  # Show or hide the paste copy action
                self.folderContextMenu.exec(self.treeWidget.viewport().mapToGlobal(position))
        else:
            self.rootContextMenu.exec(self.treeWidget.viewport().mapToGlobal(position))

    # def save_tree_to_file(self):
    #     print("saving tree to yaml file")
    def credentials_option_triggered(self):
        self.credentials_dialog = QtWidgets.QDialog()  # Create a new QDialog
        self.credentials_manager = CredentialsManagerWidget(self.credentials_dialog)  # Pass the dialog as the parent
        self.credentials_dialog.exec()  # Show the dialog

    def new_folder(self):
        # Ask for the folder name
        folder_name, ok = QtWidgets.QInputDialog.getText(self, 'New Folder', 'Enter the name of the new folder:')

        if ok and folder_name:
            # Create the folder item
            folder_item = QtWidgets.QTreeWidgetItem(self.treeWidget.invisibleRootItem())
            folder_item.setText(0, folder_name)
            self.treeWidget.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)
            # Save changes to the YAML file - uses tree as reference, so I sorted it first
            self.save_tree_to_file()

            # self.load_data_to_tree()

    def light_mode(self):
        # Code to switch to light mode
        qdarktheme.setup_theme("light")
        self.theme = "light"

    def light_dark_mode(self):
        # Code to switch to light mode
        qdarktheme.setup_theme("dark")
        qdarktheme.setup_theme(custom_colors={"primary": "#1df516"})
        self.theme = "light_dark"

    def dark_mode(self):
        # Code to switch to dark mode
        qdarktheme.setup_theme("dark")
        qdarktheme.setup_theme(custom_colors={"primary": "#1df516"})
        self.theme = "dark"

    def dark_light_mode(self):
        # Code to switch to dark mode
        qdarktheme.setup_theme("light")
        self.theme = "dark_light"

    def open_inventory_file(self, passedfile=None):
        print("open inv file")

        try:
            if passedfile is None:
                fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "YAML Files (*.yaml *.yml)")
                self.current_file = fileName
            else:
                fileName = passedfile
                self.current_file = passedfile
            print(f"reading ... {fileName}")
            if fileName:
                with open(fileName, "r", encoding="utf-8") as file:
                    data = yaml.safe_load(file)
                    self.load_data_to_tree(self.treeWidget, data)


        except Exception as e:
            print(e)
            self.notify(f"Dialog Error", f"Error: {e}")

    def save_tree_to_file(self):
        # check if a file is currently opened
        if self.current_file is None:
            print('No file currently opened')
            return

        root = self.treeWidget.invisibleRootItem()
        folder_count = root.childCount()

        data = []

        for i in range(folder_count):
            folder_item = root.child(i)
            folder_dict = {
                'folder_name': folder_item.text(0),
                'sessions': [],
            }

            session_count = folder_item.childCount()
            for j in range(session_count):
                session_item = folder_item.child(j)
                session_dict = session_item.refBinding
                folder_dict['sessions'].append(session_dict)

            data.append(folder_dict)

        with open(self.current_file, 'w') as file:  # use self.current_file here
            yaml.dump(data, file)

    def open_menu(self, position):
        self.current_item = self.treeWidget.itemAt(position)
        if self.current_item is not None and self.current_item.parent() is not None:  # if the item has a parent, it's a session
            self.context_menu.exec(self.treeWidget.viewport().mapToGlobal(position))

    def get_all_creds(self):
        conn = sqlite3.connect('settings.sqlite')
        c = conn.cursor()
        c.execute('SELECT displayname, id FROM creds order by displayname')
        creds = c.fetchall()
        conn.close()
        return creds

    def get_one_creds(self, id):
        conn = sqlite3.connect('settings.sqlite')
        c = conn.cursor()
        c.execute(f'SELECT username, password FROM creds where id={id}')
        creds = c.fetchone()
        conn.close()
        return creds

    def on_action_connect(self):
        print("Connect...")

        current_selected = self.treeWidget.currentItem()
        creds = self.get_all_creds()
        # Show the dialog
        dlgSelectCreds = Ui_dlgSelectCreds(creds, current_selected)
        dlgSelectCreds.exec()

        # Get selected id
        selected_id = dlgSelectCreds.get_selected_cred()
        if selected_id == 0:
            return
        # Use the id here
        print(f"Selected ID: {selected_id}")

        use_creds = self.get_one_creds(selected_id)
        username = use_creds[0]
        encrypted_password = use_creds[1]
        unencrypted_password = cryptonomicon(encrypted_password)

        print(f"Properties: {current_selected.refBinding}")
        host = str(current_selected.refBinding['host'])
        if not self.is_ssh_open(host, current_selected.refBinding.get('port', '22'), 5):
            self.notify("Connection Failure", f"Unable to quick connect on port {current_selected.refBinding.get('port', '22')}")
            return

        hostinfo = {
            "host": current_selected.refBinding['host'],
            "port": current_selected.refBinding.get('port', '22'),
            "username": username,
            "password": unencrypted_password,
            "log_filename": f"./logs/session_{current_selected.refBinding['host']}.log",
            "theme": self.theme
        }

        try:
            self.stackedWidget.setCurrentIndex(1)
            ssh_widget = qtssh_widget((hostinfo, self))
            ssh_widget.setObjectName("ssh_widget")

            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(ssh_widget)

            # Create new tab and add SSH widget
            new_tab = QtWidgets.QWidget()
            new_tab.setLayout(layout)

            ssh_widget.setVisible(True)
            # Add the new tab and set its title to the host
            index = self.twTerminals.addTab(new_tab, hostinfo['host'])

            # Set the new tab as the current tab
            self.twTerminals.setCurrentIndex(index)
        except:
            pass

    def is_ssh_open(self, hostname, port=22, timeout=5):
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            # Try to connect to the SSH port (22)
            sock.connect((hostname, int(port)))
            # If the connection succeeds, the SSH port is open
            return True
        except socket.error:
            # If the connection fails, the SSH port is closed
            return False
        finally:
            # Always close the socket
            sock.close()

    class PropertyDialog(QtWidgets.QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setFixedWidth(600)
            self.layout = QtWidgets.QVBoxLayout(self)
            self.text_edit = QtWidgets.QTextEdit(self)
            self.layout.addWidget(self.text_edit)
            self.setLayout(self.layout)

        def set_properties(self, properties):
            self.text_edit.setText(properties)

        def copy_to_clipboard(self):
            clipboard = QtCore.QApplication.clipboard()
            clipboard.setText(self.text_edit.toPlainText())

    def on_action_display_properties(self):
        current_selected = self.treeWidget.currentItem()
        if current_selected is not None:
            if current_selected.refBinding.get('credsid') is None:
                credsid = 0
            else:
                credsid = current_selected.refBinding['credsid']
            info = self.get_one_creds(credsid)
            if info is not None:
                username = info[0]
            else:
                username = "no default"
            properties = f"Host: {current_selected.refBinding['host']}\nDefault Username: {username}"

            try:
                properties = ""
                ref = current_selected.refBinding.items()
                for k, v in ref:
                    if k != "password":
                        properties += f"{k}:{v}\n"
            except:
                pass

            self.dialog = self.PropertyDialog()
            self.dialog.set_properties(properties)
            self.dialog.exec()

    def load_data_to_tree(self, tree_widget, data, root_item=None):
        # Parse the YAML data into a Python list of dictionaries

        # Sort the data by folder name
        data.sort(key=lambda d: d['folder_name'])

        # Within each folder, sort the sessions by display name
        for folder in data:
            folder['sessions'].sort(key=lambda d: d['display_name'])

        self.treeWidget.clear()
        if root_item is None:
            root_item = tree_widget.invisibleRootItem()
        for site in data:
            site_item = QTreeWidgetItem()
            site_item.setText(0, site["folder_name"])
            root_item.addChild(site_item)
            for session in site["sessions"]:
                session_item = QTreeWidgetItem()
                session_item.setText(0, session["display_name"])
                bindRef = {}
                for key, value in session.items():
                    if key == "credsid" and value is None:
                        bindRef[key] = 0

                    bindRef[key] = value
                session_item.refBinding = bindRef
                site_item.addChild(session_item)
        # Collapsing all the nodes after building the tree
        for i in range(root_item.childCount()):
            tree_widget.collapseItem(root_item.child(i))
        self.treeWidget.setHeaderLabel("Sessions")
        self.treeWidget.setHeaderHidden(False)

    def new_session(self):
        try:

            dialog = NewSessionDialog()
            result = dialog.exec()

            if result == QtWidgets.QDialog.DialogCode.Accepted:
                if dialog.sshKeyCheckBox.isChecked():
                    hostinfo = {
                        "host": dialog.hostLineEdit.text(),
                        "port": dialog.hostPortEdit.text(),
                        "username": dialog.usernameLineEdit.text(),
                        "pkey_path": dialog.pkeyLineEdit.text(),
                        "log_filename": dialog.logLineEdit.text(),
                        "theme": self.theme
                    }
                else:
                    hostinfo = {
                        "host": dialog.hostLineEdit.text(),
                        "port": dialog.hostPortEdit.text(),
                        "username": dialog.usernameLineEdit.text(),
                        "password": dialog.passwordLineEdit.text(),
                        "log_filename": dialog.logLineEdit.text(),
                        "theme": self.theme
                    }
            else:
                return
            self.stackedWidget.setCurrentIndex(1)
            try:
                ssh_widget = qtssh_widget((hostinfo, self))
                ssh_widget.setObjectName("ssh_widget")

                layout = QtWidgets.QVBoxLayout()
                layout.addWidget(ssh_widget)

                # Create new tab and add SSH widget
                new_tab = QtWidgets.QWidget()
                new_tab.setLayout(layout)

                ssh_widget.setVisible(True)
                # Add the new tab and set its title to the host
                index = self.twTerminals.addTab(new_tab, hostinfo['host'])

                # Set the new tab as the current tab
                self.twTerminals.setCurrentIndex(index)
            except:
                pass


        except Exception as e:
            print(e)
            self.notify(f"Connection Failed", f"Error: : {e}")

    def close_tab(self, index):
        # Confirmation dialog
        confirm = QtWidgets.QMessageBox()
        confirm.setWindowTitle('Disconnect')
        confirm.setText('Are you sure you want to close?')
        confirm.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        confirm.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        ret = confirm.exec()

        if ret == QtWidgets.QMessageBox.StandardButton.Yes:
            # Get the widget from the tab
            tab_widget = self.twTerminals.widget(index)

            # Close the SSH session (assuming there's a close method in the ssh_widget class)
            # Modify this as per your implementation of qtssh_widget
            tab_widget.close()

            # Remove the tab
            self.twTerminals.removeTab(index)

    def notify(self, message, info):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(info)
        msg.setWindowTitle(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()


from PyQt6 import QtWidgets, QtCore


class NewSessionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New SSH Session")

        # Create layout and form
        self.layout = QtWidgets.QFormLayout(self)

        self.hostLineEdit = QtWidgets.QLineEdit(self)
        self.hostLineEdit.setText("10.0.0.12")

        self.hostPortEdit = QtWidgets.QLineEdit(self)
        self.hostPortEdit.setText("22")

        self.usernameLineEdit = QtWidgets.QLineEdit(self)
        self.usernameLineEdit.setText("admin")

        self.passwordLineEdit = QtWidgets.QLineEdit(self)
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.sshKeyCheckBox = QtWidgets.QCheckBox("Use SSH Keyfile", self)
        self.sshKeyCheckBox.stateChanged.connect(self.validate_inputs)

        # SSH Key Path with file chooser button
        sshKeyPathLayout = QtWidgets.QHBoxLayout()
        self.pkeyLineEdit = QtWidgets.QLineEdit(self)
        self.pkeyLineEdit.setContentsMargins(0, 0, 0, 0)
        self.pkeyLineEdit.setText("C:/Users/97685/.ssh/id_rsa")
        sshKeyPathLayout.addWidget(self.pkeyLineEdit)

        self.fileChooserButton = QtWidgets.QToolButton(self)
        self.fileChooserButton.setContentsMargins(0, 0, 0, 0)
        self.fileChooserButton.setIcon(QtGui.QIcon("./icons/folder.png"))
        self.fileChooserButton.clicked.connect(self.open_file_dialog)
        sshKeyPathLayout.addWidget(self.fileChooserButton)

        self.logLineEdit = QtWidgets.QLineEdit(self)
        self.logLineEdit.setText("./logs/session.log")

        # Add rows
        self.layout.addRow("Host", self.hostLineEdit)
        self.layout.addRow("Port", self.hostPortEdit)
        self.layout.addRow("Username", self.usernameLineEdit)
        self.layout.addRow("Password", self.passwordLineEdit)
        self.layout.addRow("Use SSHKey File?", self.sshKeyCheckBox)
        self.layout.addRow("Key Path", sshKeyPathLayout)
        self.layout.addRow("Log Filename", self.logLineEdit)

        # Buttons
        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel, self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addRow(self.buttonBox)

    def validate_inputs(self):
        if not self.sshKeyCheckBox.isChecked():
            if self.passwordLineEdit.text().strip() == "":
                QtWidgets.QMessageBox.warning(self, "Validation Error",
                                              "Password is required when 'Use SSH Keyfile' is not checked.")

    def open_file_dialog(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select SSH Key File")
        if file_name:
            self.pkeyLineEdit.setText(file_name)


if __name__ == "__main__":
    import sys, os
    if not os.path.isfile('crypto.key'):
        generate_key()

    if not os.path.isfile('settings.sqlite'):
        create_db()

    app = QtWidgets.QApplication(sys.argv)
    import qdarktheme

    # global_theme_type = "light"
    # global_theme_type = "light_dark"
    global_theme_type = "dark"
    # global_theme_type = "dark_light"

    if global_theme_type == "light_dark" or global_theme_type == "dark":
        outer_theme = "dark"
        qdarktheme.setup_theme("dark")
        qdarktheme.setup_theme(custom_colors={"primary": "#1df516"})
    elif global_theme_type == "dark_light":
        outer_theme = "light"
        qdarktheme.setup_theme(outer_theme)
    else:
        outer_theme = global_theme_type
        qdarktheme.setup_theme(outer_theme)

    global_theme = global_theme_type

    Ui_UglyPTY = QtWidgets.QMainWindow()
    ui = UtlyPty()
    ui.setupUi(Ui_UglyPTY)
    Ui_UglyPTY.show()
    sys.exit(app.exec())
