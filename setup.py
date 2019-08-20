from distutils.core import setup

package             = ['arhuaco']

service_packages    = ['arhuaco.service']

sensors_packages = ['arhuaco.sensors',
                    'arhuaco.sensors.source',
                    'arhuaco.sensors.util']

analysis_packages   = ['arhuaco.analysis',
                       'arhuaco.analysis.util',
                       'arhuaco.analysis.convolutional',
                       'arhuaco.analysis.optimization',
                       'arhuaco.analysis.features',
                       'arhuaco.analysis.generative',
                       'arhuaco.analysis.svm']

backend_packages = ['arhuaco.backend']

response_packages   = ['arhuaco.response']

graphics_packages   = ['arhuaco.graphics']

training_packages   = ['arhuaco.training']

test_packages       = ['arhuaco.test']

config_packages     = ['arhuaco.config']

setup(
        name = 'arhuaco',
        version = '0.1',
        packages = package
                   +service_packages
                   +sensors_packages
                   +analysis_packages
                   +backend_packages
                   +graphics_packages
                   +response_packages
                   +training_packages
                   +test_packages
                   +config_packages,
        license = 'Apache 2.0',
        platforms = ['Linux'],
        maintainer = 'Andres Gomez (kurono)',
        maintainer_email = 'kurono@riseup.net',
     )
