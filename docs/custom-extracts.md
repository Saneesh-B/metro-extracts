# Create a custom Metro Extract

Is the location you're looking for not on the extract list? Mapzen hosts the top 200 of the world's most popular metro areas available for immediate download, but also allows for the creation of custom extracts.

![Map of Popular Extracts](./images/extracts_map.png)

## Custom Extract walkthrough

1. Go to the Metro Extracts download page at https://mapzen.com/data/metro-extracts/
2. Type in the location you want a custom extract for. You'll see the geographic hierarchy of the feature in the dropdown menu, allowing you to make a more precise extract.

    ![Custom Extract Dropdown Menu](./images/custom_searchbar.png)

3. Once you've selected a place from the dropdown menu, a solid blue bounding box will appear on the map. You can drag this to specify the boundaries of the extract. You'll see in the example below, that if you request a custom extract near a popular extract, you'll see a red line outlining the popular extract.

    ![Selecting a custom extract on the map](./images/customextract.png)

4. After you have the custom extract ready, press the 'Get Extract' button.
5. You'll be prompted to either sign up or sign in with a Mapzen Developer account. This uses [GitHub](https://www.github.com) authentication (if you don't have a GitHub account, you can sign up for one at: [https://github.com/join](https://github.com/join))
6. Custom extracts can take about 30-60 minutes to generate, depending on the size. An email will be sent to the address associated with your GitHub account, but will also be viewable on the Metro Extracts page under 'your custom extracts'. This page also shows you the status of the custom extract and allows you to access previous requests as well.
![Pending custom extracts](./images/your_custom_extracts.png)