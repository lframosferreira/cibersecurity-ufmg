local au = vim.api.nvim_create_autocmd
local ag = vim.api.nvim_create_augroup

local file = vim.fn.expand("%:p")
local output = vim.fn.expand("%:r")

vim.o.makeprg = "pandoc -t beamer " .. file .. " -o " .. output .. ".pdf"

au("BufWritePost", {
	desc = "Compile Pandoc",
	group = ag("project", {}),
	pattern = "*.md",
	command = "Make",
})

require("ufo").setup({
	provider_selector = function(_, filetype, _)
		if filetype == "markdown" then
			return { "treesitter", "indent" }
		end
		return { "lsp", "indent" }
	end,
})
