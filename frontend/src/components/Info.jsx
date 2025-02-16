import React, { useState, useEffect } from 'react';
import "../App.css";
import ItemInfo from './ItemInfo';

function Info() {

//   const [messages, setMessages] = useState([])
const [messages, setMessages] = useState([{'item': 'Leather Wallet', 'impact': ['Deforestation: Leather production often contributes to deforestation for cattle ranching to source the leather.', 'Greenhouse Gas Emissions: Cattle farming releases methane, a potent greenhouse gas.', 'Water Pollution: Tanning processes use chemicals that can pollute water sources.', 'Chemical Use: The tanning process involves chemicals that can be harmful to the environment and human health.', 'Energy Consumption: The manufacturing process can be energy-intensive, contributing to carbon emissions.'], 'current_impact': ['Continued environmental impact due to deforestation and greenhouse gas emissions if leather continues to be used.'], 'alternatives': [{'name': 'Cork Wallet', 'company': 'N/A', 'logo': 'N/A', 'description': 'Cork is a sustainable and renewable material harvested from the bark of cork oak trees without harming the tree. Cork wallets are durable and environmentally friendly.', 'link': 'https://www.etsy.com/market/cork_wallet'}, {'name': 'Vegan Leather Wallet', 'company': 'N/A', 'logo': 'N/A', 'description': 'Vegan leather is made from plant-based materials or synthetic alternatives, avoiding animal products. Materials like pineapple leaf fiber, recycled plastic, and other sustainable materials.  There are many options that are better for the environment.', 'link': 'https://www.amazon.com/s?k=vegan+leather+wallet'}, {'name': 'Recycled Materials Wallet', 'company': 'N/A', 'logo': 'N/A', 'description': 'Wallets made from recycled materials, such as recycled plastic or other waste materials, reduce waste and environmental impact. These can be a good alternative to buying new.', 'link': 'https://www.amazon.com/s?k=recycled+material+wallet'}, {'name': 'DIY Fabric Wallet', 'company': 'N/A', 'logo': 'N/A', 'description': 'Create a wallet from fabric scraps, old clothing, or other materials. This reduces waste and lets you customize the wallet.', 'link': 'https://www.youtube.com/watch?v=7LqF1iL8sC0'}]}, {'item': 'Monster Energy Ultra Blue Hawaiian', 'impact': ['Aluminum Production: Mining bauxite ore for aluminum can manufacturing causes deforestation and soil erosion. The smelting process uses a lot of energy, often from fossil fuels, leading to greenhouse gas emissions.', 'Manufacturing Processes: Production of energy drinks includes the use of water, energy, and other raw materials (sweeteners, flavors, etc.). These processes can contribute to pollution and resource depletion. High fructose corn syrup as a common ingredient uses corn, and the use of fertilizers can cause an environmental impact as well.', 'Packaging and Waste: Aluminum cans are recyclable, but recycling rates vary. If cans end up in landfills, they can take a long time to degrade. Additionally, the transport and distribution of these drinks contribute to carbon emissions.', 'Ingredient Sourcing: The sourcing of ingredients may involve land use changes, and the use of pesticides and fertilizers, which could have environmental impacts. Specifics depend on the ingredients used.', 'Water Usage: The production of energy drinks requires water for various stages, which can stress local water resources if not managed efficiently.', 'Carbon Footprint: Production, transportation, and disposal of energy drinks result in greenhouse gas emissions and contribute to climate change.'], 'current_impact': ['Waste from packaging: Many cans still end up in landfills.', 'Carbon Emissions: Shipping and manufacturing of this product has carbon emissions.'], 'alternatives': [{'name': 'Zevia', 'company': 'Zevia LLC', 'logo': 'N/A', 'description': "Zevia offers energy drinks that use natural sweeteners and no artificial ingredients. It's a better option because it avoids some of the health concerns associated with artificial sweeteners and additives.", 'link': 'https://www.zevia.com/'}, {'name': 'Make Your Own Energy Drink', 'company': 'N/A', 'logo': 'N/A', 'description': 'Create your own energy drink using natural ingredients like fruit, green tea, or coffee, and natural sweeteners like honey or maple syrup. This way you control the ingredients and packaging waste.', 'link': 'N/A'}]}, {'item': 'mirror', 'impact': ['Manufacturing creates a lot of CO2 emissions due to the energy needed and by products of the manufacturing process. ', 'Manufacturing uses a lot of water in the process.', 'Shipping causes emissions and uses fuel', 'Manufacturing glass requires a lot of heat, which can result in high energy consumption and greenhouse gas emissions.'], 'current_impact': ['The mirror can reflect light and energy, which may contribute to environmental impact, depending on its placement and use. The manufacturing process of the mirror may also have an environmental impact.', 'If the mirror is broken, it is not biodegradable and can end up in landfills, which have negative impacts on the environment.', 'The manufacturing and disposal of mirrors can contribute to the consumption of resources and waste generation. '], 'alternatives': [{'name': 'Mirror made with recycled materials', 'company': 'N/A', 'logo': 'N/A', 'description': 'Made with recycled materials, this item is more environmentally friendly by using less virgin resources.', 'link': 'N/A'}, {'name': 'Use a second-hand mirror', 'company': 'N/A', 'logo': 'N/A', 'description': 'Reuse a mirror, which reduces the need for new production and waste.', 'link': 'N/A'}, {'name': 'Reduce use of mirrors.', 'company': 'N/A', 'logo': 'N/A', 'description': 'Reduce the use of mirrors to help reduce manufacturing', 'link': 'N/A'}]}]);
  const [messageComponents, setMessageComponents] = useState([]);
  const [isStreaming, setIsStreaming] = useState(true);

  useEffect(() => {
    const eventSource = new EventSource("http://localhost:8080/stream_api");

    eventSource.onmessage = (event) => {
      let parsedData;
      try {
        parsedData = JSON.parse(event.data);
      } catch (error) {
        parsedData = event.data;
      }

      if (typeof parsedData === "object" && parsedData.status === "stop") {
        setIsStreaming(false);
        eventSource.close();
      }

      setMessages(prevMessages => [...prevMessages, parsedData]);
      console.log(parsedData)

      setMessageComponents(prevComponents => [...prevComponents, parsedData.item ? <ItemInfo key={Date.now()}
                                                                           label={parsedData.item}
                                                                           impact={parsedData.impact}
                                                                           current_impact={parsedData.current_impact}
                                                                           alternatives={parsedData.alternatives} /> : null]);
    };

    eventSource.onerror = (error) => {
      console.error("EventSource error:", error);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, []);

  return (
    <div className="Info">
      {/* <h2>API Messages</h2> */}
      {/* {isStreaming ? <p>Streaming data...</p> : <p>Streaming stopped.</p>} */}
      {/* <div className="ItemWrapper">{messageComponents}</div> */}

      <div className="ItemSection">
        <ul className="ItemWrapper">
          {messages.map((msg, index) => (
              <div key={index}>
                  <ItemInfo label={msg.item} impact={msg.impact} current_impact={msg.current_impact} alternatives={msg.alternatives} />
              </div>
          ))}
        </ul>
      </div>

    </div>
  );
}

export default Info;