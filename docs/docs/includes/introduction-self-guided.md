## Self-Guided Learners

These instructions are for self-guided learners who do not have access to a pre-configured lab environment. Follow these steps to set up your environment and begin the workshop.

## Introduction

This workshop is designed to teach you how to use Reasoning Models, like DeepSeek R1 and utilize tools and Reflection style architecture with LangChain to do deep research. It consists of multiple labs, each highlighting a specific feature of the process of building a deep researcher. The labs are meant to be completed in order, as each one builds on the knowledge and work from the previous lab.

## Prerequisites

1. Access to an Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/){:target="_blank"} before you begin.
1. You need a GitHub account. If you don’t have one, create it at [GitHub](https://github.com/join){:target="_blank"}.

## Open the Workshop

The preferred way to run this workshop is using GitHub Codespaces. This option provides a pre-configured environment with all the tools and resources needed to complete the workshop. Alternatively, you can open the workshop locally using a Visual Studio Code Dev Container.

=== "GitHub Codespaces"

    Select **Open in GitHub Codespaces** to open the project in GitHub Codespaces.

    [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/BUILD25-LAB331){:target="_blank"}

    !!! Warning "Building the Codespace will take several minutes. You can continue reading the instructions while it builds."

## Authenticate with Azure

You need to authenticate with Azure so the agent app can access the Azure AI Agents Service and models. Follow these steps:

1. Ensure the Codespace has been created.
1. In the Codespace, open a new terminal window by selecting **Terminal** > **New Terminal** from the **VS Code menu**.
1. Run the following command to authenticate with Azure:

    ```shell
    az login --use-device-code
    ```

    !!! note
        You'll be prompted to open a browser link and log in to your Azure account. Be sure to copy the authentication code first.

        1. A browser window will open automatically, select your account type and click **Next**.
        2. Sign in with your Azure subscription **Username** and **Password**.
        3. **Paste** the authentication code.
        4. Select **OK**, then **Done**.

    !!! warning
        If you have multiple Azure tenants, then you will need to select the appropriate tenant when authenticating.

        ```shell
        az login --use-device-code --tenant <tenant_id>
        ```

1. Next, select the appropriate subscription from the command line.
1. Leave the terminal window open for the next steps.

## Deploy the Azure Resources

The following resources will be created in the `rg-deep-research-workshop` resource group in your Azure subscription.

- An **Azure AI Foundry hub** named **deep-research-wksp**
- An **Azure AI Foundry project** named **Deep Research Workshop**
- A **Serverless (pay-as-you-go) DeepSeek R1 model deployment** named **gpt-4o (Global 2024-08-06)**. See pricing details [here](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="_blank"}.

We have provided a bash script to automate the deployment of the resources required for the workshop. Alternatively, you may deploy resources manually using Azure AI Foundry studio. Select the desired tab.
