local function is_tex(format)
  return format == 'tex' or format == 'latex'
end

function RawBlock(el)
  if is_tex(el.format) then
    local label = el.text:match('^\\label{(.+)}$')
    if label then
      return pandoc.RawBlock('html', '<span id="' .. label .. '"></span>')
    end
  end
end

function RawInline(el)
  if is_tex(el.format) then
    local label = el.text:match('^\\label{(.+)}$')
    if label then
      return pandoc.RawInline('html', '<span id="' .. label .. '"></span>')
    end
  end

  if is_tex(el.format) then
    local pageref = el.text:match('^\\pageref{(.+)}$')
    if pageref then
      return {}
    end
  end
end

function Link(el)
  local target = el.target
  local label = target:match('^%./(.+)%.md$')
  if label then
    local kebab = label:gsub('([a-z])([A-Z])', '%1-%2')
                       :gsub('([A-Z])([A-Z][a-z])', '%1-%2')
                       :lower()
    el.target = '#' .. kebab
    return el
  end
end
