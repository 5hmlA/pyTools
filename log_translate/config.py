from business.bluetooth_translator import BluetoothTranslator
from log_translator import SysLogTranslator

translates = [SysLogTranslator(translators=[BluetoothTranslator()])]
