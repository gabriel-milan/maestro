class EnumStringification( object ):
  "Adds 'enum' static methods for conversion to/from string"

  _ignoreCase = False

  @classmethod
  def tostring(cls, val):
    "Transforms val into string."
    from Gaugi.utilities  import get_attributes
    for k, v in get_attributes(cls, getProtected = False):
      if v==val:
        return k
    return None

  @classmethod
  def fromstring(cls, str_):
    "Transforms string into enumeration."
    from Gaugi.utilities  import get_attributes
    if not cls._ignoreCase:
      return getattr(cls, str_, None)
    else:
      allowedValues = [attr for attr in get_attributes(cls) if not attr[0].startswith('_')]
      try:
        idx = [attr[0].upper() for attr in allowedValues].index(str_.upper().replace('-','_'))
      except ValueError:
        raise ValueError("%s is not in enumeration. Use one of the followings: %r" % (str_, allowedValues) )
      return allowedValues[idx][1]

  @classmethod
  def retrieve(cls, val):
    """
    Retrieve int value and check if it is a valid enumeration string or int on
    this enumeration class.
    """
    from Gaugi.utilities import get_attributes
    allowedValues = [attr for attr in get_attributes(cls) if not attr[0].startswith('_')]
    try:
      # Convert integer string values to integer, if possible:
      val = int(val)
    except ValueError:
      pass
    if type(val) is str:
      oldVal = val
      val = cls.fromstring(val)
      if val is None:
          raise ValueError("String (%s) does not match any of the allowed values %r." % \
              (oldVal, allowedValues))
    else:
      if not val in [attr[1] for attr in allowedValues]:
        raise ValueError(("Attempted to retrieve val benchmark "
            "with a enumeration value which is not allowed. Use one of the followings: "
            "%r") % allowedValues)
    return val

  @classmethod
  def sretrieve(cls, val):
    "Return enumeration equivalent value in string if it is a valid enumeration code."
    return cls.tostring(cls.retrieve(val))

  @classmethod
  def optionList(cls):
    from operator import itemgetter
    from Gaugi.utilities import get_attributes
    return [v for v in sorted(get_attributes( cls, getProtected = False), key=itemgetter(1))]

  @classmethod
  def stringList(cls):
    from operator import itemgetter
    from Gaugi.utilities import get_attributes
    return [v[0] for v in sorted(get_attributes( cls, getProtected = False), key=itemgetter(1))]

  @classmethod
  def intList(cls):
    from operator import itemgetter
    from Gaugi.utilities import get_attributes
    return [v[1] for v in sorted(get_attributes( cls, getProtected = False), key=itemgetter(1))]

class Color(EnumStringification):
	CEND      = '\33[0m'
	CBOLD     = '\33[1m'
	CITALIC   = '\33[3m'
	CURL      = '\33[4m'
	CBLINK    = '\33[5m'
	CBLINK2   = '\33[6m'
	CSELECTED = '\33[7m'
	CBLACK  = '\33[30m'
	CRED    = '\33[31m'
	CGREEN  = '\33[32m'
	CYELLOW = '\33[33m'
	CBLUE   = '\33[34m'
	CVIOLET = '\33[35m'
	CBEIGE  = '\33[36m'
	CWHITE  = '\33[37m'
	CBLACKBG  = '\33[40m'
	CREDBG    = '\33[41m'
	CGREENBG  = '\33[42m'
	CYELLOWBG = '\33[43m'
	CBLUEBG   = '\33[44m'
	CVIOLETBG = '\33[45m'
	CBEIGEBG  = '\33[46m'
	CWHITEBG  = '\33[47m'
	CGREY    = '\33[90m'
	CRED2    = '\33[91m'
	CGREEN2  = '\33[92m'
	CYELLOW2 = '\33[93m'
	CBLUE2   = '\33[94m'
	CVIOLET2 = '\33[95m'
	CBEIGE2  = '\33[96m'
	CWHITE2  = '\33[97m'
	CGREYBG    = '\33[100m'
	CREDBG2    = '\33[101m'
	CGREENBG2  = '\33[102m'
	CYELLOWBG2 = '\33[103m'
	CBLUEBG2   = '\33[104m'
	CVIOLETBG2 = '\33[105m'
	CBEIGEBG2  = '\33[106m'
	CWHITEBG2  = '\33[107m'