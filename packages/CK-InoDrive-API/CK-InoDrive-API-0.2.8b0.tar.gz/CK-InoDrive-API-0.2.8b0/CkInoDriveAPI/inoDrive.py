import logging

from .defines import CK
from .wsHandle import InoDriveWS
from .file import InoDriveFile
from .discoverWs import InoDriveDiscoverWs
from .userApp import InoDriveUserApp


class InoDrive(object):
    """
    Main InoDrive API Class.

    :Arguments: ****kwargs** *(Dict)*:

       * **target** *(String)*: InoDrive target identifier (Name, Serial Number, or IPv4 Address).
       * **autoConnect** *(Boolean)*: True or False value to automatically have the Module connect.
    :Returns: **Object** - An Object that can manage the Module's Connection, File's, and Main User Application.
    """
    def __init__(self, **kwargs):
        logging.debug('Create InoDrive instance...')
        self._auto_connect = kwargs.get('autoConnect', False)

        self._connection_handle = InoDriveWS(**kwargs)
        if self._auto_connect:
            self._connection_handle.connect()

        self._id_file = InoDriveFile(connection_handle=self._connection_handle, **kwargs)
        self._id_discover = InoDriveDiscoverWs(connection_handle=self._connection_handle, **kwargs)
        self._id_user_app = InoDriveUserApp(connection_handle=self._connection_handle, **kwargs)
        logging.debug('Instance created...')

    def __del__(self):
        self.dispose()

    def dispose(self):
        """
        Disposes InoDrive Connection Handle and User Application Instance.

        :Arguments: **self** *(Object)*: Reference to InoDrive object.
        :Returns: None
        """
        if self._id_user_app:
            self._id_user_app.dispose()

        if self._connection_handle:
            self._connection_handle.dispose()

    def on(self, *args, **kwargs):
        return self._connection_handle.on(*args, **kwargs)

    def connected(self):
        """
        Retrieve InoDrive Connection Handle Status.

        :Arguments: **self** *(Object)*: Reference to InoDrive Object to use Connection Handle Instance.
        :Returns: **Boolean** - True or False Value on having an established Connection Handle.
        """
        return self._connection_handle.connected

    def connect(self, timeout=None):
        """
        Have InoDrive's Connection Handle attempt to establish a connection.

        :Arguments:
           * **self** *(Object)*: Reference to InoDrive Object to use Connection Handle Instance.
           * **timeout** *(Number)*: Optional timeout value in seconds.
        :Returns: **Boolean** - True or False Value on successfully establishing a connection.
        """
        return self._connection_handle.connect(timeout)

    def disconnect(self, timeout=None):
        """
        Have InoDrive's Connection Handle attempt to disconnect.

        :Arguments:
           * **self** *(Object)*: Reference to InoDrive Object to use Connection Handle Instance.
           * **timeout** *(Number)*: Optional timeout value in seconds.
        :Returns: **Boolean** - True or False Value on successfully disconnecting from the Module.
        """
        return self._connection_handle.disconnect(timeout)

    def set_target(self, target=None):
        """
        Change InoDrive Object's target module.

        :Arguments:
           * **self** *(Object)*: Reference to InoDrive Object to use Connection Handle Instance.
           * **target** *(String)*: A Module Name, Serial Number, or IPv4 Address.
        :Returns: Nothing
        """
        if self._connection_handle:
            self._connection_handle.set_target(target)

    def get_discover_info(self, *args, **kwargs):
        """
        Get InoDrive Module and Network Information.

        :Arguments:
           * **self** *(Object)*: Reference to InoDrive Object to use Connection Handle Instance.
           * ***args** *(Tuple)*: Non-Keyword Arguments.
           * ****kwarg** *(Dict)*: Keyword Arguments.
        :Returns: **Dict** - A Dictionary containing the InoDrive's Module and Network Information.
        """
        return self._id_discover.discover(*args, **kwargs)

    def delete_uapp(self):
        """
        Deletes current running User Application.

        :Arguments: **self** *(Object)*: Reference to InoDrive Object to use internal File Instance.
        :Returns: **Boolean** - True or False Value on successfully deleting the User Application File.
        """
        return self._id_file.delete_uapp()

    def file_read(self, *args, **kwargs):
        """
        Read file(s) operation from InoDrive with provided file path and content type.

        :Arguments:
           * **self** *(Object)*: Reference to InoDrive Object to use internal File Instance.
           * ***args** *(Tuple or List)*: A single Dictionary or a List of Dictionaries to iterate through. Each entry needs a file path and content type ('json' or 'string').
           * ****kwarg** *(Dict)*: Keyword Arguments.
        :Returns: **List** - A List of Dictionaries with either JSON or String UTF-8 content. If only one file, Returns first element in the List.
        """
        return self._id_file.read(*args, **kwargs)

    def file_write(self, *args, **kwargs):
        """
        Write file(s) operation to InoDrive with provided file path and content object.

        :Arguments:
           * **self** *(Object)*: Reference to InoDrive Object to use internal File Instance.
           * ***args** *(Tuple or List)*: A single Dictionary or a List of Dictionaries to iterate through. Each entry needs a file path and content blob in Raw Binary.
           * ****kwarg** *(Dict)*: Keyword Arguments.
        :Returns: **Boolean** - True or False Value on successfully writing file out.
        """
        return self._id_file.write(*args, **kwargs)

    def upload_user_app(self, content=None):
        """
        Upload User Application File to InoDrive.

        :Arguments:
           * **self** *(Object)*: Reference to InoDrive Object to use internal File Instance.
           * **content** *(Bytes)*: Raw Binary content blob of User Application File.
        :Returns: **Boolean** - True or False Value on successfully writing User Application File.
        """
        try:
            return self.file_write({'path': "/uapp/application.idsol", 'content': content}, CK.FILE.UAPP_TRANSFER)
        except Exception as ex:
            logging.exception(ex)

    def upload_firmware(self, content=None):
        """
        Upload Firmware File to InoDrive.

        :Arguments:
           * **self** *(Object)*: Reference to InoDrive Object to use internal File Instance.
           * **content** *(Bytes)*: Raw Binary content blob of Firmware File.
        :Returns: **Boolean** - True or False Value on successfully writing Firmware File.
        """
        try:
            return self.file_write({'path': "/firmware/firmware.nhfw", 'content': content}, CK.FILE.FIRMWARE_TRANSFER)
        except Exception as ex:
            logging.exception(ex)

    def read_module_config(self):
        """
        Get module configuration file.

        :Arguments: **self** *(Object)*: Reference to InoDrive Object to use internal File Instance.
        :Returns: **Dict** - Dictionary that contains Module Name, Network Properties, and Electrical Properties.
        """
        try:
            return self.file_read({'path': '/config/module_cfg.json', 'content': 'json'})
        except Exception as ex:
            logging.exception(ex)

    def write_module_config(self, content=None):
        """
        Write out to Module's Configuration File. All Changes to File require the InoDrive to be powered cycled to take effect.

        :Arguments:
           * **self** *(Object)*: Reference to InoDrive Object to use internal File Instance.
           * **content** *(Bytes)*: Raw Binary content blob.
        :Returns: **Boolean** - True or False Value on successfully writing out the Module Configuration File.
        """
        try:
            if type(content) != dict:
                logging.error('Content type is not dictionary')
                return False

            return self.file_write({'path': '/config/module_cfg.json', 'content': content})
        except Exception as ex:
            logging.exception(ex)

    # User Application Poll
    def start_poll(self, *args, **kwarg):
        """
        Start polling User Application to update Variable List.

        :Arguments:
           * **self** *(Object)*: Reference to InoDrive Object to use internal User Application Instance.
           * ***args** *(Tuple)*: Non-Keyword Arguments.
           * ****kwarg** *(Dict)*: timeout *(Number)* -> Optional timeout for Variable List polling in seconds.
        :Returns: Nothing
        """
        return self._id_user_app.start_poll(*args, **kwarg)

    def stop_poll(self):
        """
        Stop polling User Application for Variable List update.

        :Arguments: **self** *(Object)*: Reference to InoDrive Object to use internal User Application Instance.
        :Returns: Nothing
        """
        return self._id_user_app.stop_poll()

    def get_variable(self, *args, **kwargs):
        """
        Get a single Variable that is set to Read or Read/Write in User Application, does not poll Variable List.

        :Arguments:
           * **self** *(Object)*: Reference to InoDrive Object to use internal User Application Instance.
           * ***args** *(Tuple)*: Argument for either variable Name *(String)* or ID *(Integer)*.
           * ****kwarg** *(Dict)*: Keyword Arguments.
        :Returns: **Dict**: Dictionary containing Variable's ID, Type, Access Level, Value, and Write Permission.
        """
        return self._id_user_app.get_variable(*args, **kwargs)

    def get_all_variables(self, *args, **kwargs):
        """
        Get All Variable(s) that are set to Read or Read/Write in User Application.

        :Arguments:
           * **self** *(Object)*: Reference to InoDrive Object to use internal User Application Instance.
           * ***args** *(Tuple)*: Non-Keyword Arguments.
           * ****kwarg** *(Dict)*: Keyword Arguments.
        :Returns: **Dict** - Dictionary containing timestamp and a List of all Read or Read/Write Variable(s).
        """
        return self._id_user_app.get_all_variables(*args, **kwargs)

    def get_variable_list(self, *args, **kwargs):
        """
        Get All Variable(s) name's that are set to Read or Read/Write in User Application.

        :Arguments:
           * **self** *(Object)*: Reference to InoDrive Object to use internal User Application Instance.
           * ***args** *(Tuple)*: Non-Keyword Arguments.
           * ****kwarg** *(Dict)*: Keyword Arguments.
        :Returns: **List** - List of all Variable name's that are set to Read or Read/Write.
        """
        return self._id_user_app.get_variable_list(*args, **kwargs)

    def read_var(self, *args, **kwargs):
        """
        Read Variable(s) value by Name or ID in User Application, polls User Application Variable List.

        :Arguments:
            * **self** *(Object)*: Reference to InoDrive Object to use internal User Application Instance.
            * ***args** *(Tuple or List)*: Argument can be a single Variable Name (String) or a ID (Integer). Can also be a List of Variable Name's or ID's.
            * ****kwarg** *(Dict)*: Keyword Arguments.
        :Returns: **Variable (Boolean, Integer, Floating Point) or Dict:**

            * If argument is a single Variable Name or ID -> Returns the variable value.
            * If argument is a List of Variable Name's or ID's -> Returns Dictionary of Variable name's paired with their value.
        """
        return self._id_user_app.read_var(*args, **kwargs)

    def write_var(self, *args, **kwargs):
        """
        Write Variable(s) with new value out to User Application, polls User Application Variable List.

        :Arguments:
            * **self** *(Object)*: Reference to InoDrive Object to use internal User Application Instance.
            * ***args** *(Tuple)*: Variable Name (string) or ID (integer) and the new value.
            * ****kwarg** *(Dict)*: Keyword Arguments.
        :Returns: **Boolean** - True or False on successfully writing new Variable value out to User Application.
        """
        return self._id_user_app.write_var(*args, **kwargs)

    def get_var(self, *args, **kwargs):
        """
        Get Variable(s) value by name or id in User Application, does not poll User Application Variable List.

        :Arguments:
            * **self** *(Object)*: Reference to InoDrive Object to use internal User Application Instance.
            * ***args** *(Tuple or List)*: Argument can be a single Variable Name (String) or a ID (Integer). Can also be a List of Variable Name's or ID's.
            * ****kwarg** *(Dict)*: Keyword Arguments.
        :Returns: **Variable (Boolean, Integer, Floating Point) or Dict:**

           * If argument is a single Variable Name or ID -> Returns the Variable value.
           * If argument is a List of Variable's Name's or ID's -> Returns Dictionary of Variable Name's paired with their value.
        """
        return self._id_user_app.get_var(*args, **kwargs)

    def set_var(self, *args, **kwargs):
        """
        Set Variable(s) with new value out to User Application, does not poll User Application Variable List.

        :Arguments:
            * **self** *(Object)*: Reference to InoDrive Object to use internal User Application Instance.
            * ***args** *(Tuple)*: Variable Name (String) or ID (Integer) and the new value.
            * ****kwarg** *(Dict)*: Dictionary of Variable name's or id's paired with their new value.
        :Returns: **Boolean** - True or False on successfully writing new Variable value out to User Application.
        """
        return self._id_user_app.set_var(*args, **kwargs)

