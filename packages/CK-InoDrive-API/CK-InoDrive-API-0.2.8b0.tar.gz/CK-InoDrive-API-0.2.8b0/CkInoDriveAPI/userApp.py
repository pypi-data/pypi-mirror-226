import time
import json
import datetime
import logging
import threading

from .defines import CK
from .utils import Utils
from .wsHandle import InoDriveWS


class InoDriveUserApp(object):
    """
    User Application Class, management of User Application file.

    :Arguments: ****kwargs** *(Object)*: InoDrive Object with an established Connection Handle.
    :Returns: **Object** - An Object that can manage the main User Application.
    """
    def __init__(self, **kwargs):
        self._connection_handle: InoDriveWS = kwargs.get('connection_handle')
        self._poll_timeout = kwargs.get('poll_timeout', 1)

        self._thread = None
        self._keep_running = False

        self._var_list_updated = False
        self._var_values_updated = False

        self._variable_values = {}
        self._program_id = None
        self._ntp_poll_time = 0

    def __del__(self):
        self.dispose()

    def dispose(self):
        """
        Dispose Process thread for Polling User Application.

        :Arguments: **self** *(Object)*: Reference to User Application Instance.
        :Returns: None
        """
        self.stop_poll()

    def start_poll(self, timeout=None):
        """
        Create Process Thread to poll User Application's Variable Listing.

        :Arguments:
            * **self** *(Object)*: Reference to User Application Instance.
            * **timeout** *(Number)*: Optional timeout property for updating Variable List in seconds.
        :Returns: None
        """
        if self._thread:
            return

        self._thread = threading.Thread(target=self._thread_loop, daemon=True)
        self._thread.start()

        # Wait until variable list is updated so we can have all variables available
        if timeout:
            self._poll_timeout = timeout

        timeout = (self._poll_timeout * 2) * 100

        while (self._var_list_updated is False or self._var_values_updated is False) and timeout > 0:
            timeout -= 1
            time.sleep(0.01)

    def stop_poll(self):
        """
        Stop's Process Thread to poll User Application's Variable Listing.

        :Arguments: **self** *(Object)*: Reference to User Application Instance.
        :Returns: None
        """
        if not self._thread:
            return

        self._keep_running = False
        self._thread.join()
        self._thread = None

    def get_variable_list(self, access=None):
        """
        Get list of Variable Name's in User Application that are set to Read or Read/Write.

        :Arguments:
            * **self** *(Object)*: Reference to User Application Instance.
            * **access** *(String)*: Optional argument to get Variable Name's that are set to 'read' or 'readWrite'.
        :Returns: **List**: Returns a List of all Variable Name's that are set to Read or Read/Write.
        """
        try:
            if self._connection_handle.connected and self._var_list_updated is False:
                self.update_variable_list()

            var_list = []

            if access is None:
                access = [CK.API_VAR_ACCESS['read'], CK.API_VAR_ACCESS['readWrite']]

            if type(access) != list:
                access = list(access)

            for var_name, var_props in self._variable_values.items():
                if access and var_props['access'] in access:
                    var_list.append(var_name)

            return var_list
        except Exception as ex:
            logging.exception(ex)

        return []

    def get_variable(self, id=None):
        """
        Get specific Variable in User Application that are set to Read or Read/Write by Name or ID. Does not poll Variable List.

        :Arguments:
            * **self** *(Object)*: Reference to User Application Instance.
            * **id** *(String or Integer)*: Argument to get Variable by either it's Name or ID.
        :Returns: **Dict**: Dictionary containing Variable's ID, Type, Access Level, Value, and Write Permission.
        """
        try:
            for var_name, var_props in self._variable_values.items():
                if type(id) == str and id == var_name:
                    return var_props
                if type(id) == int and var_props['id'] == id:
                    return var_props

        except Exception as ex:
            logging.exception(ex)

        return None

    def get_all_variables(self):
        """
        Get all Variable(s) in User Application that are set to Read or Read/Write. Does not poll Variable List.

        :Arguments: **self** *(Object)*: Reference to User Application Instance.
        :Returns: **Dict**: Dictionary containing all Variable's with their ID's, Type's, Access Level's, Value's, and Write Permission's.
        """
        result = {
            'timestamp': self._ntp_poll_time,
            'items': {},
        }

        for var_name, var_props in self._variable_values.items():
            result['items'].update({var_name: {
                'id': var_props['id'],
                'access': CK.API_VAR_ACCESS[var_props['access']],
                'type': var_props['type'],
                'value': var_props['value'],
            }})

        return result

    def update_variable_list(self):
        """
        Sends message to Module to Update all Read or Read/Write Variable Listing.

        :Arguments: **self** *(Object)*: Reference to User Application Instance.
        :Returns: **Boolean**: True or False value on Updating the Variable Listing.
        """
        try:
            self._var_list_updated = False
            self._var_values_updated = False

            msg = Utils.get_tlv(CK.SPECIAL.JSON_API)
            msg += Utils.get_tlv(CK.TYPE.STRING, {'id': Utils.get_token(8, bytes=False), 'request': CK.JSON_API.VAR_LIST})

            resp = self._connection_handle.request(msg)

            if resp.get('error'):
                logging.error(f'Retrieving variables list failed...')
                return False

            if len(resp['items']) > 0:
                if resp['items'][0]['ctpType'] != CK.TYPE.STRING:
                    logging.error('Unsupported response type...')
                    return False

                json_response = json.loads(resp['items'][0]['data'])

                self._program_id = json_response['program_id']
                self._update_variables_list(json_response['data'])
                self._var_list_updated = True

        except Exception as ex:
            logging.exception(ex)

        return False

    def read_var(self, argv=None, **kwargs):
        """
        Read Variable(s) value by name or id in User Application, polls Variable List.

        :Arguments:
            * **self** *(Object)*: Reference to User Application Instance.
            * **argv** *(Tuple or List)*: Argument can be a single Variable Name (String) a Variable ID (Integer) or a list of Variable Name's or ID's.
            * ****kwarg** *(Dict)*: Keyword Arguments.
        :Returns: **Variable (Boolean, Integer, Floating Point) or Dict:**

            * If argument is a single Variable Name or ID -> Returns the Variable value.
            * If argument is a List of Variable Name's or ID's -> Returns Dictionary of Variable Name's paired with their value.
        """
        try:
            if self._connection_handle.connected and self._var_list_updated is False:
                self.update_variable_list()

            var_list = []
            request_data = []
            resp_dict = {}

            if type(argv) == str or type(argv) == int:
                var_list.append(argv)

            if type(argv) == list:
                var_list = argv

            for var_name in var_list:
                variable = self.get_variable(var_name)
                if variable:
                    request_data.append({'id': variable['id']})

            if len(request_data) == 0:
                return None

            msg = Utils.get_tlv(CK.SPECIAL.JSON_API)
            msg += Utils.get_tlv(CK.TYPE.STRING, {'id': Utils.get_token(8, bytes=False), 'request': CK.JSON_API.VAR_ACCESS, 'data': request_data})

            resp = self._connection_handle.request(msg)

            if resp.get('error'):
                logging.error(f'Retrieving variables data...')
                return None

            if len(resp['items']) <= 0 or resp['items'][0]['ctpType'] != CK.TYPE.STRING:
                logging.error('Unsupported response type...')
                return None

            json_response = json.loads(resp['items'][0]['data'])

            for item in json_response['data']:
                variable = self.get_variable(item['id'])
                if variable:
                    var_name = self._get_variable_name_by_id(variable['id'])

                    precision = kwargs.get('floatPrecision')
                    if (variable['type'] == 'float' or variable['type'] == 'double') and type(precision) == int:
                        var_value = round(variable['value'], precision)
                    else:
                        var_value = item['val']

                    variable['value'] = var_value

                    resp_dict.update({var_name: var_value})

            if len(resp_dict) > 0:
                if type(argv) == list:
                    return resp_dict
                else:
                    return list(resp_dict.values())[0]
        except Exception as ex:
            logging.exception(ex)

        return None

    def write_var(self, argv=None, value=None, **kwarg):
        """
        Write Variable(s) with new value out to User Application, polls Variable List.

        :Arguments:
            * **self** *(Object)*: Reference to User Application Instance.
            * **argv** *(Tuple)*: Variable Name (String) or ID (Integer).
            * **value** *(Boolean, Integer, Floating Point)*: New value to be written out to Variable.
            * ****kwarg** *(Dict)*: Keyword Arguments.
        :Returns: **Boolean** - True or False on successfully writing new Variable value out to User Application.
        """
        try:
            if self._connection_handle.connected and self._var_list_updated is False:
                self.update_variable_list()

            if argv is None:
                return False

            var_dict = {}
            request_data = []

            if type(argv) == str or type(argv) == int:
                if value is None:
                    return False

                var_dict.update({argv: value})
            elif type(argv) == dict:
                var_dict = argv
            else:
                return False

            for var_name, var_value in var_dict.items():
                variable = self.get_variable(var_name)
                if variable:
                    is_c_type = Utils.is_proper_c_type(var_value, variable['type'])
                    if is_c_type:
                        variable['value'] = var_value
                        request_data.append({'id': variable['id'], 'val': var_value})

            msg = Utils.get_tlv(CK.SPECIAL.JSON_API)
            msg += Utils.get_tlv(CK.TYPE.STRING, {'id': Utils.get_token(8, bytes=False), 'request': CK.JSON_API.VAR_ACCESS, 'data': request_data})

            resp = self._connection_handle.request(msg)

            if resp.get('error'):
                logging.error(f'Retrieving variables data...')
                return None

            if len(resp['items']) <= 0 or resp['items'][0]['ctpType'] != CK.TYPE.STRING:
                logging.error('Unsupported response type...')
                return None

            json_response = json.loads(resp['items'][0]['data'])

            if json_response.get('result') == 'Success':
                return True
            else:
                return False

        except Exception as ex:
            logging.exception(ex)

        return False

    def get_var(self, argv=None, **kwargs):
        """
        Get Variable(s) value by name or id in User Application, does not poll Variable List.

        :Arguments:
            * **self** *(Object)*: Reference to User Application Instance.
            * **argv** *(Tuple or List)*: Argument can be a single Variable Name (String) or a ID (Integer) or a list of Variable Name's or ID's.
            * ****kwarg** *(Dict)*: Keyword Arguments.
        :Returns: **Variable (Boolean, Integer, Floating Point) or Dict:**

           * If argument is a single Variable Name or ID -> Returns the Variable value.
           * If argument is a List of Variable's Name's or ID's -> Returns Dictionary of Variable Name's paired with their value.
        """
        try:
            var_list = []
            res = {}

            if type(argv) == str or type(argv) == int:
                var_list.append(argv)

            if type(argv) == list:
                var_list = argv

            for var_name in var_list:
                variable = self.get_variable(var_name)
                if variable and variable.get('value') is not None:
                    precision = kwargs.get('floatPrecision')
                    if (variable['type'] == 'float' or variable['type'] == 'double') and type(precision) == int:
                        res.update({var_name: round(variable['value'], precision)})
                    else:
                        res.update({var_name: variable['value']})

            if len(res) > 0:
                if type(argv) == list:
                    return res
                else:
                    return list(res.values())[0]
        except Exception as ex:
            logging.exception(ex)

        return None

    def set_var(self, argv=None, value=None, **kwargs):
        """
        Set Variable(s) with new value out to User Application, does not poll Variable List.

        :Arguments:
            * **self** *(Object)*: Reference to User Application Instance.
            * **argv** *(Tuple)*: Variable Name (String) or ID (Integer).
            * **value** *(Boolean, Integer, Floating Point)*: New Value to be written out to Variable.
            * ****kwarg** *(Dict)*: Dictionary of Variable Name's or ID's paired with their new value.
        :Returns: **Boolean** - True or False on successfully writing new Variable value out to User Application.
        """
        try:
            if argv is None:
                return False

            vars = {}

            if type(argv) == str or type(argv) == int:
                if value is None:
                    return False

                vars.update({argv: value})
            elif type(argv) == dict:
                vars = argv
            else:
                return False

            for var_name, var_value in vars.items():
                variable = self.get_variable(var_name)
                if variable:
                    is_c_type = Utils.is_proper_c_type(var_value, variable['type'])
                    if is_c_type:
                        variable.update({
                            'value': var_value,
                            'write': True,
                        })

            return True
        except Exception as ex:
            logging.exception(ex)

        return False

    def _get_variable_name_by_id(self, id=None):
        if id is None:
            return None

        for var_name, var_props in self._variable_values.items():
            if var_props['id'] == id:
                return var_name

        return None

    def _update_variables_list(self, variable_list=None):
        try:
            if variable_list is None:
                return

            # Remove all old variables which are no longer in the user application
            items_to_remove = []
            for var_name, var_data in self._variable_values.items():
                in_var_list = False
                for item in variable_list:
                    if var_name == item['name']:
                        in_var_list = True
                        continue

                if not in_var_list:
                    items_to_remove.append(var_name)

            for var_name in items_to_remove:
                self._variable_values.pop(var_name, None)

            # Create new or refresh variables if they do not exist already
            for item in variable_list:
                variable = self._variable_values.get(item['name'])
                if not variable:
                    self._variable_values.update({item['name']: {
                        'id': item['id'],
                        'type': Utils.get_var_c_type(item['type']),
                        'access': item['access'],
                        'value': None,
                        'write': False,
                    }})
                else:
                    variable.update({
                        'id': item['id'],
                        'type': Utils.get_var_c_type(item['type']),
                        'access': item['access'],
                        'value': variable['value'],
                    })

        except Exception as ex:
            logging.exception(ex)

    def _thread_loop(self):
        self._keep_running = True

        last_poll_time = datetime.datetime.now() - datetime.timedelta(seconds=self._poll_timeout)
        while self._keep_running:
            try:
                curr_time = datetime.datetime.now()

                if curr_time - last_poll_time >= datetime.timedelta(seconds=self._poll_timeout):
                    begin_time = time.time()

                    # Update variable list
                    # ===========================================================================================
                    if self._var_list_updated is False or len(self._variable_values) == 0:
                        self.update_variable_list()
                    # ===========================================================================================

                    data = []
                    write_list = []

                    # Write Variables
                    # ===========================================================================================
                    for var_name in self.get_variable_list([CK.API_VAR_ACCESS['write'], CK.API_VAR_ACCESS['readWrite']]):
                        variable = self.get_variable(var_name)
                        if variable and variable['write']:
                            data.append({
                                'id': variable['id'],
                                'val': variable['value'],
                            })
                            write_list.append(variable)
                    # ===========================================================================================

                    # Read Variables
                    # ===========================================================================================
                    for var_name in self.get_variable_list([CK.API_VAR_ACCESS['read'], CK.API_VAR_ACCESS['readWrite']]):
                        variable = self.get_variable(var_name)
                        if variable:
                            data.append({
                                'id': variable['id']
                            })
                    # ===========================================================================================

                    # Retrieve the variables from the module
                    # ===========================================================================================
                    msg = Utils.get_tlv(CK.SPECIAL.JSON_API)
                    msg += Utils.get_tlv(CK.TYPE.STRING, {'id': Utils.get_token(8, bytes=False), 'request': CK.JSON_API.VAR_ACCESS, 'data': data})

                    resp = self._connection_handle.request(msg)

                    if resp.get('error'):
                        logging.error(f'Retrieving variables data...')
                        continue
                    # ===========================================================================================

                    # Variables are successfully written so now we can remove the write flag
                    for variable in write_list:
                        variable['write'] = False

                    if len(resp['items']) <= 0 or resp['items'][0]['ctpType'] != CK.TYPE.STRING:
                        logging.error('Unsupported response type...')
                        continue

                    json_response = json.loads(resp['items'][0]['data'])

                    # Check if this is new program
                    if self._program_id != json_response.get('program_id'):
                        self._var_list_updated = False
                        continue

                    # Error
                    if json_response.get('error'):
                        logging.error(json_response['error'])
                        continue

                    # Current module time
                    if json_response.get('ntpTime'):
                        self._ntp_poll_time = json_response['ntpTime']

                    # Update variable values
                    if json_response.get('data'):
                        for item in json_response['data']:
                            variable = self.get_variable(item['id'])
                            if variable:
                                variable.update({'value': item.get('val')})

                        self._var_values_updated = True

                    # Compensate the poll timeout if there was significant delay
                    time_delta = time.time() - begin_time
                    last_poll_time = curr_time - datetime.timedelta(milliseconds=time_delta)

            except Exception as ex:
                pass

            time.sleep(0.001)

