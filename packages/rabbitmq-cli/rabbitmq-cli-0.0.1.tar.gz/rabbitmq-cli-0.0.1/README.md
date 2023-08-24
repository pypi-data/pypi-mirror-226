# Custom RabbitMQ CLI

## Introduction

This Command Line Tools (CLI) allows to interact with a RabbitMQ Broker instance througth HTTP RESTFul API and offers one case for continous publishing througth AMQPS.

API Ref: https://pulse.mozilla.org/api/index.html

## Install

Install using At the command prompt, type `pip`

> pip install rabbitmqcli

## Add on

You can use an AWS Secrets Manager secret to store connection credentials. For this must define values for variables `aws.region` and `aws.secret-name`, this secret name can contains an "environment" key to change in runtime, this key must be named "env". And aditionally, enable this feature changing `default.credentials-from-secret` variable value to `True`.

### Simple secret name

> _your-secret-name_

### Secret name composed by env

> _your-secret-*{env}*-name_

For the secret structures is required the following two keys: `username` and `password`. For example:

``
{... "username": "guest", "password": "guest" ...}
``

## Configuration file

You can create a config file, or CLI will create it. This file must be named and located like this: `~/.rabbitmq-cli/config `


<table>
    <thead>
        <tr>
            <th>Sections</th>
            <th>Variables</th>
            <th>Default value</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=7>default</td>
            <td>hostname</td>
            <td>localhost</td>
            <td>.</td>
        </tr>
        <tr>
            <td>vhost</td>
            <td>/</td>
            <td>.</td>
        </tr>
        <tr>
            <td>username</td>
            <td>guest</td>
            <td>.</td>
        </tr>
        <tr>
            <td>password</td>
            <td>guest</td>
            <td>.</td>
        </tr>
        <tr>
            <td>exchange</td>
            <td>domainEvents</td>
            <td>.</td>
        </tr>
        <tr>
            <td>queue</td>
            <td>subsEvents</td>
            <td>.</td>
        </tr>
        <tr>
            <td>credentials-from-secret</td>
            <td>False</td>
            <td>.</td>
        </tr>
        <tr>
            <td rowspan=2>http</td>
            <td>port</td>
            <td>15671</td>
            <td>.</td>
        </tr>
        <tr>
            <td>ssl</td>
            <td>True</td>
            <td>.</td>
        </tr>
        <tr>
            <td rowspan=2>amqp</td>
            <td>port</td>
            <td>5671</td>
            <td>.</td>
        </tr>
        <tr>
            <td>ssl</td>
            <td>True</td>
            <td>.</td>
        </tr>
        <tr>
            <td rowspan=2>aws</td>
            <td>region</td>
            <td>us-east-1</td>
            <td>.</td>
        </tr>
        <tr>
            <td>secret-name</td>
            <td>your-{env}-secret-name</td>
            <td>.</td>
        </tr>
    </tbody>
</table>

