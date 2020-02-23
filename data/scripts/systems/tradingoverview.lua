--local originalSetData = setData
local originalOnSectorChanged = onSectorChanged

function onSectorChanged()
    originalOnSectorChanged()
    exportSectorData()
end

--[[function setData(sellable_received, buyable_received, routes_received)
	originalSetData(sellable_received, buyable_received, routes_received) -- call real function
    
    exportSectorData(sellable_received, buyable_received)
end]]--

function exportSectorData()
    local sellable, buyable = gatherData()
    --[[
	print(">Got " .. #sellable .. " sellable goods from sector " .. tostring(vec2(Sector():getCoordinates())))
	print(">Got " .. #buyable .. " buyable goods from sector " .. tostring(vec2(Sector():getCoordinates())))
	--]]

	local x, y = Sector():getCoordinates()
	local file, err = io.open("moddata/TradeExport-" .. tostring(GameSeed()) .. "-sector" .. x .. "-" .. y .. ".csv", "w")
	if file==nil then
	    file, err = io.open("moddata\\TradeExport-" .. tostring(GameSeed()) .. "-sector" .. x .. "-" .. y .. ".csv", "w")
    end
    if file==nil then
	        print("Couldn't open file: "..err)
	else

	    for _, buyoffer in pairs(buyable) do
		    writeOffer(buyoffer, file, "buy")
	    end

	    for _, selloffer in pairs(sellable) do
		    writeOffer(selloffer, file, "sell")
	    end

	    file:close()
	end
end

function writeOffer(offer, file, option)
	file:write(option .. ";")
	file:write(offer.good.name .. ";")
	file:write(offer.price .. ";")
	file:write(offer.stock .. ";")
	file:write(offer.maxStock .. ";")
	file:write(offer.coords.x .. ";")
	file:write(offer.coords.y ..";")
	file:write(offer.station%_t % offer.titleArgs .. ";")
	file:write(offer.good.size .."\n")
end

