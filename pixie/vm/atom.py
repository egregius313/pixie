import pixie.vm.object as object
from pixie.vm.code import extend, as_var
from pixie.vm.primitives import nil
import pixie.vm.stdlib as proto


class Atom(object.Object):
    _type = object.Type(u"pixie.stdlib.Atom")

    def with_meta(self, meta):
        return Atom(self._boxed_value, meta)

    def meta(self):
        return self._meta

    def with_validator(self, validator):
        return Atom(self._boxed_value, 
                    self._meta,
                    self._watch_key,
                    self._watch_fn,
                    validator=validator)
    
    def with_watch(self, watch_key, watch_fn):
        return Atom(self._boxed_value,
                    self._meta,
                    watch_key,
                    watch_fn,
                    self._validator)
    
    def __init__(self, boxed_value, 
                 meta=nil,
                 watch_key=nil, watch_fn=nil,
                 validator=nil):
        self._boxed_value = boxed_value
        self._meta = meta
        self._watch_key = watch_key
        self._watch_fn = watch_fn
        self._validator = validator


@extend(proto._reset_BANG_, Atom)
def _reset(self, v):
    assert isinstance(self, Atom)
    if self._validator is not nil:
        affirm(self._validator.invoke([v]), u"Invalid State Exception: Invalid reference state.")
    if self._watch_fn is not nil:
        self._watch_fn.invoke([self._watch_key, self, self._boxed_value, v])
    self._boxed_value = v
    return v

@extend(proto._deref, Atom)
def _deref(self):
    assert isinstance(self, Atom)
    return self._boxed_value

@extend(proto._meta, Atom)
def _meta(self):
    assert isinstance(self, Atom)
    return self.meta()

@extend(proto._with_meta, Atom)
def _with_meta(self, meta):
    assert isinstance(self, Atom)
    return self.with_meta(meta)

@extend(proto._with_watch, Atom)
def _with_watch(self, watch_key, watch_fn):
    assert isinstance(self, Atom)
    return self.with_watch(watch_key, watch_fn)

@extend(proto._with_validator, Atom)
def _with_validator(self, validate_fn):
    assert isinstance(self, Atom)
    return self.with_validator(validate_fn)

@as_var("atom")
def atom(val=nil):
    return Atom(val)
