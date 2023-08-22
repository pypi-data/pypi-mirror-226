from ovos_plugin_manager.templates.language import LanguageDetector
from lingua_podre import predict_lang, get_lang_scores


class LinguaPodrePlugin(LanguageDetector):
    def detect(self, text):
        return predict_lang(text)

    def detect_probs(self, text):
        return get_lang_scores(text)
