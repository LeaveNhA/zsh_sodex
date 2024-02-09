#!/usr/bin/env python3

import sys
import os
from guidance import models, gen, select, system, user, assistant

from contextlib import contextmanager,redirect_stderr,redirect_stdout
from os import devnull

import platform,socket,re,uuid,json,psutil,logging

ERROR_ESC = ''
MODEL_KEY = 'SODEX_PREFERRED_LLM_MODEL'
N_GPU_LAYERS_KEY = 'SODEX_LLAMA_N_GPU'
N_THREADS_KEY = 'SODEX_N_THREADS'
N_CONTEXT_KEY = 'SODEX_N_CONTEXT'
TEMPERATURE_KEY = 'SODEX_TEMPERATURE'


def getSystemInfo():
    '''
    To get system information, such as OS, CPU, etc.
    I needed to feed the model with these informations for accuracy reasons.
    '''
    try:
        info=""
        info += 'platform:' + platform.system() + '\n'
        info += 'platform-release:' + platform.release() + '\n'
        info += 'platform-version:' + platform.version() + '\n'
        info += 'architecture:' + platform.machine() + '\n'
        info += 'hostname:' + socket.gethostname() + '\n'
        info += 'ip-address:' + socket.gethostbyname(socket.gethostname()) + '\n'
        info += 'mac-address:' + ':'.join(re.findall('..', '%012x' % uuid.getnode())) + '\n'
        info += 'processor:' + platform.processor() + '\n'
        info += 'ram:' + str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB" + '\n'
        return info
    except Exception as e:
        logging.exception(e)

def get_executables_in_path():
    '''
    To get all the executable files in the PATH variable.
    I needed to feed the model with these informations for accuracy reasons.
    Simply, we cannot allow it to give us back a file that is not executable by the user.
    '''
    executables = []
    path_dirs = os.getenv("PATH").split(os.pathsep)
    for path_dir in path_dirs:
        try:
            for filename in os.listdir(path_dir):
                filepath = os.path.join(path_dir, filename)
                try:
                    if os.path.isfile(filepath) and os.access(filepath, os.X_OK):
                        executeable_name = filepath.split('/')[-1]
                        executables.append(executeable_name)
                except PermissionError:
                    # Ignore permission errors
                    pass
        except FileNotFoundError:
            # Ignore directory not found errors
            pass
    return executables

## TODO: A caching, maybe??
executables = get_executables_in_path()

class suppress_stdout_stderr_(object):
    def __enter__(self):
        self.outnull_file = open(os.devnull, 'w')
        self.errnull_file = open(os.devnull, 'w')

        self.old_stdout_fileno_undup    = sys.stdout.fileno()
        self.old_stderr_fileno_undup    = sys.stderr.fileno()

        self.old_stdout_fileno = os.dup ( sys.stdout.fileno() )
        self.old_stderr_fileno = os.dup ( sys.stderr.fileno() )

        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr

        os.dup2 ( self.outnull_file.fileno(), self.old_stdout_fileno_undup )
        os.dup2 ( self.errnull_file.fileno(), self.old_stderr_fileno_undup )

        sys.stdout = self.outnull_file
        sys.stderr = self.errnull_file
        return self

    def __exit__(self, *_):
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

        os.dup2 ( self.old_stdout_fileno, self.old_stdout_fileno_undup )
        os.dup2 ( self.old_stderr_fileno, self.old_stderr_fileno_undup )

        os.close ( self.old_stdout_fileno )
        os.close ( self.old_stderr_fileno )

        self.outnull_file.close()
        self.errnull_file.close()


class CustomChat(models.LlamaCppChat):
    def get_role_start(self, role_name, **kwargs):
      return ""

    def get_role_end(self, role_name=None):
        return "\n"

def initialize_model():
    """
    Initialize the Model with Guidance.
    """
    model_name = os.environ.get(MODEL_KEY, None)
    if model_name == None:
      ERROR_ESC = ("No model specified")
      # TODO: find a related return err code??
      exit(0)

    n_gpu_layers = os.environ.get(N_GPU_LAYERS_KEY, 1)
    # Somehow, Llama cannot use more than 2 GPU layer on MacOS with
    # Apple Silicon devices, which are simply performance cores.
    # TODO: add reference for the geeks and tracking the issue!
    n_threads = os.environ.get(N_THREADS_KEY, 2)
    n_context = os.environ.get(N_CONTEXT_KEY, 5_000)
    temperature = os.environ.get(TEMPERATURE_KEY, 1.0)

    # #001 : Bug?
    # Internally, the call goes like: CustomChat -> LlamaCpp:python-binding -> ...
    # Because of the verbose implementation on Llama internals, it uses almost the same approach
    # to suppress (or not) the output to STDERR and STDOUT.
    # To avoid a very strange debug, I verbose it and bypass it's internal dealing with STDOUT and STDERR.
    # And handle the suppression in my side of code-base.
    model = CustomChat(model_name, n_gpu_layers=n_gpu_layers, n_ctx=n_context, n_threads=n_threads, temperature=temperature, verbose=True)
    return model


with suppress_stdout_stderr_():
  model = initialize_model()
cursor_position_char = int(sys.argv[1])

# Read the input prompt from stdin.
buffer = sys.stdin.read()
full_command = buffer
llm = model

with suppress_stdout_stderr_():
  #if True:
  with system():
    llm += f"""You are a zsh shell expert named SOdex, DO help me complete the following command, you should only output the completed command, no need to include any other explanation.
    DO RESPONSE ONLY in ONE line and ONE shell command.
    Context:
    {getSystemInfo()}
"""
  with user():
    llm += full_command

  with assistant():
    llm += '$ ' + select(executables, name='app') + ' ' + gen(name='args', max_tokens=200, stop='\n')

sys.stdout.write(f"\n{llm['app']} {llm['args']}")

## Due to #001, We need to handle the deallocation output too.
## If we let it go alone, it writes to STDOUT (or maybe even STDERR)
## because of the True flag in the verbose parameter in the initialization.
with suppress_stdout_stderr_():
  del llm
  del model

sys.stdout.write(ERROR_ESC)