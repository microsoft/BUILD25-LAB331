# Getting Started

## Microsoft Build Attendees

The instructions on this page assume you are attending [Microsoft Build 2025](https://build.microsoft.com/){:target="_blank"} and have access to a pre-configured lab environment. This environment provides an Azure subscription with all the tools and resources needed to complete the workshop.

## Introduction

This workshop is designed to teach you how to use Reasoning Models, like DeepSeek R1 and utilize tools and Reflection style architecture with LangChain to do deep research. It consists of multiple labs, each highlighting a specific feature of the process of building a deep researcher. The labs are meant to be completed in order, as each one builds on the knowledge and work from the previous lab.

## Authenticate with Azure

You need to authenticate with Azure so the agent app can access the Azure AI Agents Service and models. Follow these steps:

1. Open a terminal window. The terminal app is **pinned** to the Windows 11 taskbar.

    ![Open the terminal window](../media/windows-taskbar.png){ width="300" }

2. Run the following command to authenticate with Azure:

    ```powershell
    az login
    ```

    !!! note
        You'll be prompted to open a browser link and log in to your Azure account.

        1. A browser window will open automatically, select **Work or school account** and click **Next**.

        1. Use the **Username** and **Password** found in the **top section** of the **Resources** tab in the lab environment.

        2. Select **OK**, then **Done**.

3. Then select the **Default** subscription from the command line.

4. Once you've logged in, run the following command to assign the **user** role to the resource group:

    ```powershell
    $subId = $(az account show --query id --output tsv) `
    ;$objectId = $(az ad signed-in-user show --query id -o tsv) `
    ; az role assignment create --role "f6c7c914-8db3-469d-8ca1-694a8f32e121" --assignee-object-id $objectId --scope /subscriptions/$subId/resourceGroups/"rg-agent-workshop" --assignee-principal-type 'User'
    ```

5. Stay in the terminal window for the next steps.

## Open the Workshop

Follow these steps to open the workshop in Visual Studio Code:

=== "Python"

      1. From the terminal window, execute the following commands to clone the workshop repository, navigate to the relevant folder, set up a virtual environment, activate it, and install the required packages:

          ```powershell
          git clone https://github.com/microsoft/BUILD25-LAB331.git `
          ; cd BUILD25-LAB331 `
          ; python -m venv src/.venv `
          ; src\.venv\Scripts\activate `
          ; pip install -r src/requirements.txt `
          ;
          ```

      2. Open in VS Code. From the terminal window, run the following command:

          ```powershell
          code .
          ```

        !!! warning "When the project opens in VS Code, two notifications appear in the bottom right corner. Click ✖ to close both notifications."


## Configure the Workshop

### Create the .env file

    1. **Rename** the `.env.sample` file to `.env`.

        - Select the **.env.sample** file in the VS Code **Explorer** panel.
        - Right-click the file and select **Rename**, or press <kbd>F2</kbd>.
        - Change the file name to `.env` and press <kbd>Enter</kbd>.

### Set Up Tavily API

    1. Register for a [Tavily API key](https://tavily.com/) to enable web search capabilities. This API is essential for the web research integration in Labs 2 and 3.

    2. Update the `.env` file in the project root with your Tavily API keys. Your file should now have the following line in it:

    ```
    TAVILY_API_KEY=your_tavily_api_key
    ```

## Workshop Materials

This workshop is designed as a progressive series of labs, each building on the previous one:

1. **Lab 1 (Reasoning & Model Thoughts)**: Learn how to stream the AI's thinking process in real-time and format final answers as bullet points.

2. **Lab 2 (Web Research Integration)**: Build a basic research system that generates queries, searches the web, and synthesizes the results.

3. **Lab 3 (Research Reflection)**: Extend the research capabilities with knowledge gap identification and iterative research cycles.

4. **Lab 4 (Launching Your Researcher)**: Deploy the research assistant as a web application with FastAPI and WebSockets for real-time updates.

Each lab includes code samples, explanations, and challenges to extend your learning.

## Navigation

Use the navigation menu on the left to move between labs. Each lab includes:

- An overview of what you'll learn
- Prerequisites specific to that lab
- Detailed instructions with code samples
- Explanations of key components
- Challenges to extend your learning
- Next steps to progress through the workshop

## Pro Tips

!!! tips
    1. The **Burger Menu** in the right-hand panel of the lab environment offers additional features, including the **Split Window View** and the option to end the lab. The **Split Window View** allows you to maximize the lab environment to full screen, optimizing screen space. The lab's **Instructions** and **Resources** panel will open in a separate window.
    2. If the lab instructions are slow to scroll in the lab environment, try copying the instructions’ URL and opening it in **your computer’s local browser** for a smoother experience.
    3. If you have trouble viewing an image, simply **click the image to enlarge it**.

## Next Steps

Once your environment is set up, proceed to [Lab 1: Reasoning & Model Thoughts](lab-1-reasoning-thoughts.md) to begin building your research assistant.
