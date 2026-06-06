local section_titles = {
  ['Acknowledgements'] = true,
  ['Emergency Substitutions'] = true,
  ['Essential Tools for your Kitchen'] = true,
  ['Glossary of Cooking Terms'] = true,
  ['Instant Pot Cheat Sheets'] = true,
  ['Instant Pot vs. Rice Cooker'] = true,
  ['Meal Plans'] = true,
  ['Roasted Vegetables'] = true,
  ['Staples'] = true,
}

local current_title = nil

function Header(el)
  if el.level == 1 then
    current_title = pandoc.utils.stringify(el.content)
    if section_titles[current_title] then
      return nil
    end
    return {el, pandoc.RawBlock('latex', '\\index{' .. escape_for_index(current_title) .. '}')}
  end
end

function Para(el)
  if #el.content == 1 and el.content[1].t == 'Emph' then
    local text = pandoc.utils.stringify(el.content[1])
    if is_tags(text) and current_title then
      local result = {el}
      for tag in text:gmatch('[^,]+') do
        tag = tag:match('^%s*(.-)%s*$')
        tag = tag:lower()
        table.insert(result, pandoc.RawBlock('latex',
          '\\index{' .. escape_for_index(tag) .. '!' .. escape_for_index(current_title) .. '}'))
      end
      return result
    end
  end
end

function is_tags(s)
  if #s > 100 then return false end
  if s:match('[^%w%s,&-]') then return false end
  if s:match(',') then return true end
  if #s < 30 then return true end
  return false
end

function escape_for_index(s)
  s = s:gsub('"', '""')
  s = s:gsub('!', '"!')
  s = s:gsub('|', '"|')
  s = s:gsub('@', '"@')
  s = s:gsub('\\', '\\textbackslash{}')
  s = s:gsub('{', '\\{')
  s = s:gsub('}', '\\}')
  s = s:gsub('%$', '\\$')
  s = s:gsub('&', '\\&')
  s = s:gsub('#', '\\#')
  s = s:gsub('_', '\\_')
  s = s:gsub('%^', '\\^{}')
  s = s:gsub('~', '\\~{}')
  s = s:gsub('%%', '\\%')
  return s
end
