from setuptools import setup

PLUGIN_ENTRY_POINT = 'ovos-lang-detector-plugin-lingua-podre=lingua_podre.opm:LinguaPodrePlugin'

setup(
    name='lingua_podre',
    version='0.0.3',
    packages=['lingua_podre'],
    url='https://github.com/OpenVoiceOS/lingua-podre',
    license='apache-2',
    author='JarbasAI',
    include_package_data=True,
    author_email='jarbasai@mailfence.com',
    description='dead simple word list based language detection',
    entry_points={'neon.plugin.lang.detect': PLUGIN_ENTRY_POINT}
)
