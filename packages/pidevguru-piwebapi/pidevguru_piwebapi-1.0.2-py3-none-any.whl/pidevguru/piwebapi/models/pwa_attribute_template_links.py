from pprint import pformat
from six import iteritems


class PWAAttributeTemplateLinks(object):
    swagger_types = {
        'attribute_templates': 'str',
        'categories': 'str',
        'element_template': 'str',
        'parent': 'str',
        'trait': 'str',
    }

    attribute_map = {
        'attribute_templates': 'AttributeTemplates',
        'categories': 'Categories',
        'element_template': 'ElementTemplate',
        'parent': 'Parent',
        'trait': 'Trait',
    }

    def __init__(self, attribute_templates=None, categories=None, element_template=None, parent=None, trait=None):

        self._attribute_templates = None
        self._categories = None
        self._element_template = None
        self._parent = None
        self._trait = None

        if attribute_templates is not None:
            self.attribute_templates = attribute_templates
        if categories is not None:
            self.categories = categories
        if element_template is not None:
            self.element_template = element_template
        if parent is not None:
            self.parent = parent
        if trait is not None:
            self.trait = trait

    @property
    def attribute_templates(self):
        return self._attribute_templates

    @attribute_templates.setter
    def attribute_templates(self, attribute_templates):
        self._attribute_templates = attribute_templates

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, categories):
        self._categories = categories

    @property
    def element_template(self):
        return self._element_template

    @element_template.setter
    def element_template(self, element_template):
        self._element_template = element_template

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def trait(self):
        return self._trait

    @trait.setter
    def trait(self, trait):
        self._trait = trait

    def to_dict(self):
        result = {}
        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        return result

    def to_str(self):
        return pformat(self.to_dict())

    def __repr__(self):
        return self.to_str()

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        if not isinstance(other, PWAAttributeTemplateLinks):
            return False
        return self.__dict__ == other.__dict__

