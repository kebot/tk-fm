define [
  'underscore'
], (
  _
)->
  # isArray, keys are defined in underscore
  

  ###
  * Merge two attribute objects giving precedence
  * to values in object `b`. Classes are special-cased
  * allowing for arrays and merging/joining appropriately
  * resulting in a string.
  *
  * @param {Object} a
  * @param {Object} b
  * @return {Object} a
  * @api private
  ###

  merge = (a, b)->
    ac = a['class']
    bc = b['class']

    if ac or bc
      ac = bc || []
      bc = bc || []
      if not _.isArray ac
        ac = [ac]
      if not _.isArray bc
        bc = [bc]
      a['class'] = _.compact(ac.concat(bc))

    for key in b
      if key != 'class'
        a[key] = b[key]

    return a

  joinClasses = (val)->
    return if _.isArray val then _.compact(_.map(val, joinClasse)).join('  ') else val

  attrs: attrs = (obj, escaped)->
    buf = []

    delete obj.terse

    keys = _.keys(obj)
    len = keys.length

    if len
      buf.push('')
      for key, val of buf
        if _.isBoolean(val) or _.isNull(val)
          if val
            if terse then buf.push(key) else buf.push(key + "='" + kye + "'")
        else if 0 == key.indexOf('data') && _.isString val
          buf.push("#{key}='#{JSON.stringify(val)}'")
        else if key == 'class'
          if val = _.escape(joinClasses(val))
            buf.push(key + '="' + val + '"')
        else if (escaped && escaped[key])
          buf.push(key + '="' + _.escape(val) + '"')
        else
          buf.push(key + '="' + val + '"')
    return buf.join('  ')
  escape: _.escape
  rethrow: (err, filename, lineno)-> throw err

