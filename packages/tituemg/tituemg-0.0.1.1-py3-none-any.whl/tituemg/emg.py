
import numpy as np
from scipy.signal import butter, filtfilt, iirnotch, lfilter

def low_fil(emg, cutoff_freq, sampling_rate=1000, order=2):
    """
    Aplica un filtro Butterworth de paso bajo a una señal de EMG.

    Parámetros:
    ----------
        emg (array): Señal de electromiografía (EMG) a filtrar.
        cutoff_freq (int): Frecuencia de corte del filtro en Hz.
        sampling_rate (int, opcional): Frecuencia de muestreo de la señal en Hz.
            Por defecto es 1000 Hz.
        order (int, opcional): Orden del filtro Butterworth. Por defecto es 2.

    Retorno:
    ----------
        emg_fil (array): Señal de EMG filtrada.
    """
    nyquist_freq = 0.5 * sampling_rate
    normal_cutoff = cutoff_freq / nyquist_freq
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    emg_fil = filtfilt(b, a, emg)
    return emg_fil


def rec(emg):
    """
    Realiza la rectificación de una señal de electromiografía (EMG).

    Esta función realiza la rectificación de onda completa de una señal de EMG.
    La rectificación convierte los valores negativos de la señal en sus valores
    positivos equivalentes, preservando la amplitud de la señal.

    Parámetros:
    ----------
    emg : array_like
        Señal de electromiografía de entrada.

    Retorna:
    -------
    rectified_emg : ndarray
        Señal de EMG rectificada.

    Referencias:
    -----------
    - https://numpy.org/
    """

    # Realizar la rectificación de la señal EMG
    rectified_emg = np.abs(emg - np.mean(emg))


def notch(emg, fn, fm, q=30):
    """
    Aplica un filtro notch a una señal de electromiografía (EMG).

    Esta función aplica un filtro notch a una señal de EMG para eliminar
    una frecuencia específica y sus armónicos no deseados. El filtro notch
    se crea utilizando el método de "iirnotch" de la biblioteca SciPy y se
    aplica a la señal de entrada utilizando el método "lfilter".

    Parámetros:
    ----------
    emg : array_like
        Señal de electromiografía de entrada.
    fn : float
        Frecuencia central del filtro notch en Hz.
    fm : float
        Frecuencia de muestreo de la señal en Hz.
    q : float, opcional
        Factor de calidad del filtro notch (predeterminado: 30).

    Retorna:
    -------
    filtered_emg : ndarray
        Señal de EMG filtrada con el filtro notch aplicado.

    Referencias:
    -----------
    - https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.iirnotch.html
    - https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.lfilter.html
    """

    # Crear coeficientes del filtro notch
    b, a = iirnotch(fn, q, fm)

    # Aplicar filtro notch a la señal de EMG
    filtered_emg = lfilter(b, a, emg)

    return filtered_emg


def normalizacion(emg, cvm):
    """
    Normaliza una señal de electromiografía (EMG) en relación a un valor máximo conocido.

    Esta función realiza la normalización de una señal de EMG con su contraccio voluntaria maxima(CVM). es decir que expresa todos los valores
    de esta como porsentaje de la cvm.

    Parámetros:
    ----------
    emg : array_like
        Señal de electromiografía a normalizar.
    cvm : array_like o float
        Señal de electromiografía de la prueva de contraccion voluntaria maxima(CVM) o el valor maximo de activacion durante la prueba.

    Retorna:
    -------
    emg_norm : ndarray
        Señal de EMG normalizada.

    Referencias:
    -----------
    - [Referencia a la normalización de señales EMG]

    """

    # Realizar la normalización de la señal EMG
    emg_norm = (emg / np.max(cvm)) * 100

    return emg_norm


def raw_to_env(emg, fil, cvm=False, fc=1000, orden=2):
    """
    Convierte una señal de electromiografía (EMG) cruda en su envolvente.

    Esta función toma una señal de EMG cruda y realiza los siguientes pasos:
    1. Rectifica la señal para obtener su valor absoluto.
    2. Aplica un filtro paso bajo Butterworth para obtener la envolvente de la señal rectificada.
    3. Opcionalmente, normaliza la envolvente en relación a un valor máximo conocido (CVM).

    Parámetros:
    ----------
    emg : array_like
        Señal de electromiografía cruda a procesar.
    fil : int
        Frecuencia de corte del filtro paso bajo en Hz.
    cvm : array_like, opcional
        Valor máximo conocido (CVM) para la normalización. Si no se proporciona, no se normaliza.
    fc : int, opcional
        Frecuencia de muestreo de la señal en Hz (por defecto es 1000 Hz).
    orden : int, opcional
        Orden del filtro Butterworth (por defecto es 2).

    Retorna:
    -------
    emg_env : ndarray
        Envolvente de la señal de EMG procesada.

    Referencias:
    -----------
    - [Referencia a la técnica de envolvente de señal EMG]

    """


    # Rectificar la señal EMG
    emg_rec = np.abs(emg - np.mean(emg))

    # Crear coeficientes del filtro paso bajo Butterworth
    b, a = butter(int(orden), (int(fil) / (fc / 2)), btype="low")

    # Aplicar filtro paso bajo a la señal rectificada
    emg_env = filtfilt(b, a, emg_rec)

    # Normalizar la envolvente si se proporciona el CVM
    if cvm:
        cvm_rec = np.abs(cvm - np.mean(cvm))
        cvm_env = filtfilt(b, a, cvm_rec)
        emg_env = (emg_env / np.max(cvm_env)) * 100

    return emg_env
