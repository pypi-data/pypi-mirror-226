import subprocess

class Trait():
    """
    Description for class.

    :ivar target_dict: Argument mapping for target arguments
    :ivar option_dict: Argument mapping for option arguments
    :ivar command_seq: Sequence of commands to execute
    """
    
    _command_seq = []
    _target_dict = {}
    _option_dict = {}
    
    def _option(self, flag_dict: dict, key_list: list):
        """ Maps user defined text to literal cli arguements 

        Parameters
        ----------
        flag_dict : dict-like mapping
            Mapping of user-defined terms to cli arguements
        key_list : list-like of arguments
            List of user-defined terms to pass
        """
        
        if isinstance(key_list, str):
            key_list = [key_list]
            
        sub_seq = []

        for item in key_list:

            flag = flag_dict.get(item, None)

            if flag is not None:
                sub_seq.append(f" {flag}")

        return sub_seq
   
    def target(self, key_list: list):
        """First set of arguments for command (if any).

        Parameters
        ----------
        key_list : list-like of arguments
            Command arguments to pass
        """
        
        sub_seq = self._option(_target_dict, key_list)
        self._command_seq.extend(sub_seq)
        
        return self
        
    def options(self, key_list: list):
        """Final set of options for command (if any).

        Parameters
        ----------
        key_list : list-like of arguments
            Command arguments to pass
        """
        
        sub_seq = self._option(_option_dict, key_list)
        self._command_seq.extend(sub_seq)
        
        return self._execute(self._command_seq)
    
    def _execute(self, command_list: list):
        """Do describe either series or dataframe.

        Parameters
        ----------
        command_list : list-like of arguments
            Complete list of arguments / options to pass to command
        """
        
        proc = subprocess.run(command_list, text=True, capture_output=True)
        
        return command_list, proc.stdout
