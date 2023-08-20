# apispec-helper

This project provides objective oriented helper classes collection for defining OpenAPI objects in [apispec](https://pypi.org/project/apispec/).

> **_NOTE:_** OpenAPI Specification version supported by this project is [3.0.3](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md).

## Overview

In general, when using apispec to create OpenAPI Specifications, we pass OpenAPI Objects to core APIs through Python Dictionary:

```python
spec.components.schema(
    "Gist",
    {
        "properties": {
            "id": {"type": "integer", "format": "int64"},
            "name": {"type": "string"},
        }
    },
)
```
```python
spec.path(
    path="/gist/{gist_id}",
    operations=dict(
        get=dict(
            responses={"200": {"content": {"application/json": {"schema": "Gist"}}}}
        )
    ),
)
```

This approach is simple and straightforward. We can easily construct arbitrary OpenAPI Objects in this structure. However, it's not easy to reuse/extend these objects. Consider a paginated Response Object with the following schema:
```yaml
components:
  schemas:
    Pets:
      properties:
        result_count:
          type: integer
        next_page_url:
          type: string
        previous_page_url:
          type: string
        data:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
```

We'll create Dictionary below for apispec

```python
spec.components.schema(
    "Pets",
    {
        "properties": {
            "result_count": {"type": "integer"},
            "next_page_url": {"type": "string"},
            "previous_page_url": {"type": "string"},
            "data": {
                "type": "array",
                "items": {
                    "type":"object",
                    "properties":{
                        "id": {"type": "integer"}, "name":{"type": "string"}
                    }
                } 
            }
        }
    }
)
```
However, in real world, everything won't be that simple. For instance, if most APIs' response in our application are paginated(e.g., automatically wrapped by backend middleware like [Django REST framework](https://www.django-rest-framework.org/)), then the pagination metadata field, `result_count` / `next_page_url` / `previous_page_url`, will appear everywhere in source code. Though we can prevent the issue by create functions or class for help, we still need to maintain these utilities by ourselves.

Another disadvantage of the Dictionary approach is we need to lookup fields' definition for OpenAPI Objects. As [OpenAPI Specification](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#parameter-object) shows, there are hundreds of fields among different OpenAPI Objects. We need to construct Python dictionaries carefully to prevent us from providing wrong values. It is not a trivial work especially if there are hundreds of OpenAPI Objects or deeply nested OpenAPI Objects defined in our specification. We need a better approach can help us manage field types and provide hints/auto-completion when writing specification.

To address these disadvantage of using Dictionary to represent OpenAPI Objects, **apispec-helper** implements OpenAPI Objects definition with native Python Classes. We also provide helper Classes to simplify works when working with OpenAPI Objects and apispec. 

For instance, with **apispec-helper**, we can rewrite the `Pets` example:

```python
class PaginatedData(ComponentBase):
    def __init__(self, data_schema: Object):
        super().__init__(
            component_definition=Object(
                properties={
                    "result_count": Integer(),
                    "next_page_url": String(),
                    "previous_page_url": String(),
                    "data": data_schema
                },
            )
        )


class Pet(ComponentBase):
    def __init__(self):
        super().__init__(
            component_definition=Object(
                properties={
                    "id": Integer(),
                    "name": String()
                },
            )
        )


class PaginatedPet(PaginatedData):
    def __init__(self):
        super().__init__(
            data_schema=Array(
                description="Array of SupportedCurrency",
                items=Pet().component_name
            )
        )

# ... snip
        
spec.components.schema(
    Pet().component_name, Pet().component_definition
)

spec.components.schema(
    PaginatedPet().component_name, PaginatedPet().component_definition
)
```
It will generate result yaml like:
```yaml
components:
  schemas:
    Pet:
      properties:
        id:
          type: integer
        currency_code:
          type: string
    PaginatedPet:
      properties:
        result_count:
          type: integer
        next_page_url:
          type: string
        previous_page_url:
          type: string
        data:
          items:
            $ref: '#/components/schemas/Pet'
          type: array
      type: object
```

You can use any Object-Oriented approaches supported by Python with **apispec-helper**. Fields are explicitly defined in each helper classes instead of using `**kwargs`, which means modern Python IDEs(e.g., [PyCharm](https://www.jetbrains.com/pycharm/) and [VSCode](https://code.visualstudio.com/)) can generate hints and auto-complete your codes. Also, typing hints can help you pass correct Objects to fields(modern IDEs can check parameter types for you). 

![Auto-Complete](/docs/images/auto_complete.png)

## How to use

### Installation

This project is released on PyPI([Project Page](https://pypi.org/project/apispec-helper/)). To install the latest version from PyPI

```shell
pip install -u apispec-helper
```

### Basics

**apispec-helper** already provides pre-defined OpenAPI Objects, which are categorized into 3 submodules:

- basic_type
- component
- path

| Submodule  | Class                 | OpenAPI Object                |
|------------|-----------------------|-------------------------------|
| basic_type | Example               | Example Object                |
| basic_type | ExternalDocumentation | External Documentation Object |
| basic_type | Server                | Server Object                 |


| Submodule | Class          | OpenAPI Object         | Note                                                                                                                                                                                                                                                                                   |
|-----------|----------------|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| component | Encoding       | Encoding Object        |                                                                                                                                                                                                                                                                                        |
| component | MediaType      | Media Type Object      |                                                                                                                                                                                                                                                                                        |
| component | Header         | Header Object          | - It can be a circular reference for `content` field, so we define data type as `dict[str, str]` for convenience <br>- You can use pre-defined `component.ParameterStyle` enum's value for `style` field                                                                               |
| component | Encoding       | Encoding Object        |                                                                                                                                                                                                                                                                                        |
| component | Link           | Link Object            |                                                                                                                                                                                                                                                                                        |
| component | Parameter      | Parameter Object       | - You can use pre-defined `component.ParameterStyle` Class's member for `style` field<br>- You can use pre-defined `component.ParameterLocation` enum's value for `in_` field<br>- You can use pre-defined `component.CommonMediaTypeName` for `content` field as content type name    |
| component | MediaType      | Media Type Object      | - You can use pre-defined `component.CommonMediaTypeName` Class's member for                                                                                                                                                                                                           |
| component | RequestBody    | Request Body Object    | - You can use pre-defined `component.CommonMediaTypeName` Class's member for `content` field as content type name                                                                                                                                                                      |
| component | Response       | Response Object        | - You can use pre-defined `component.CommonMediaTypeName` Class's member for `content` field as content type name                                                                                                                                                                      |
| component | SecurityScheme | Security Scheme Object | - You can use pre-defined `comopnent.SecuritySchemeType` Class's member value for `type_` field<br>- You can use pre-defined `component.HTTPAuthenticationScheme` enum's value for `scheme` field<br>- You can use pre-defined `component.APIKeyLocation` enum's value for `in_` field |
| component | OAuthFlow      | OAuth Flow Object      |                                                                                                                                                                                                                                                                                        |


| Submodule | Class     | OpenAPI Object   | Note                                                                                                                                                                             |
|-----------|-----------|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| path      | PathItem  | PathItem Object  | All Operations(`get` / `put` / `post` / `delete` / `options` / `head` / `patch` / `trace`) are defined through `Operations` Class to be compatible with apispec core APIs' input |
| path      | Operation | Operation Object |                                                                                                                                                                                  | 

And basic schema typing helper classes

| Submodule  | Class   | Note                                                                                                                          |
|------------|---------|-------------------------------------------------------------------------------------------------------------------------------|
| basic_type | Object  | For Schema Object `type: "object"`                                                                                            |
| basic_type | OneOf   | For Schema Object `type: "oneOf`                                                                                              |
| basic_type | Boolean | For Schema Object `type: "boolean`                                                                                            |
| basic_type | Null    | For Schema Object `type: "null`                                                                                               |
| basic_type | Array   | For Schema Object `type: "array`                                                                                              |
| basic_type | String  | For Schema Object `type: "string`. You can use pre-defined `comonent.PreDefineStringFormat` Class's value for `format_` field |
| basic_type | Number  | For Schema Object `type: "number`. You can use pre-defined `comonent.NumberFormat` Class's value for `format_` field          |
| basic_type | Integer | For Schema Object `type: "integer`. You can use pre-defined.`comonent.IntegerFormat` Class's value for `format_` field        |
| basic_type | OneOf   | For Schema Object `type: "oneOf`                                                                                              |
| basic_type | OneOf   | For Schema Object `type: "oneOf`                                                                                              |

Remember that what **apispec-helper** does is still creating dictionary for apispec core APIs, but isn't changing apispec's behavior. To convert these Python Class Objects to Dictionary, you can use `dict()` build-in method. Thus, you can provide these Classes Objects as parameters as below:

```python
from apispec_helper.basic_type import Object, Integer, IntegerFormat, String
from apispec import APISpec

pet = Object(
    properties={
        "id": Integer(format_=IntegerFormat.INT64),
        "name": String(maxLength=16, minLength=1)
    },
)

spec = APISpec(
    openapi_version="3.0.3",
    title="Tsinn",
    version="1.0.0"
)

spec.components.schema(
    "Pet", dict(pet)
)
```

### Base Class Helper

It can be redundant to import and call `dic()` repeatedly each time calling apispec core APIs. Also, it takes extra efforts on managing input parameters to apispec core APIs, as apispec doesn't directly accept OpenAPI Objects as input. Therefore, **apispec-helper** provides 2 Bases Classes, `ComponentBase` and `PathBase`, to simplify these works.

#### `ComponentBase`

The `ComponentBase` is used as interface to generate input for `spec.component` related apispec core APIs. It accepts only 1 argument, `component_definition`:

```python
class Pet(ComponentBase):
    def __init__(self):
        super().__init__(
            component_definition=Object(
                properties={
                    "id": Integer(),
                    "name": String()
                },
            )
        )
```

After implementing it, child class will have 2 properties, `component_name` and `component_definition`, which return child class name as component name and OpenAPI Object dictionary, respectively:

```python
# return "Pet" as string
Pet().component_name

# return 
# {
#     "type": "object", 
#     "properties": {
#         "id": {
#             "type": "integer"
#         }, 
#         "name": {
#             "type": "string"
#         }
#     }
# }
Pet().component_definition
```
They can be used as `component_id` and `component` for `APISpec.component` core APIs.

```python
spec.component.schema(
    Pet().component_name, Pet().component_definition
)
```

To simplify API call, `ComponentBase` also provides a special property, `apispec_parameter`, to generate dictionary of parameters which apispec core APIs require:

```python
spec.component.schema(**Pet().apispec_parameter)
```

#### `PathBase` 

The `PathBase` is used as interface to generate input for `APISpec.path` related apispec core APIs. It accepts 2 arguments, `path` and `path_item_definition`:

```python
class GetPetAPI(PathBase):
    def __init__(self):
        super().__init__(
            path="/pet",
            path_item_definition=PathItem(
                Operations(
                    get=Operation(
                        responses={
                            "200": Response(
                                content={
                                    CommonMediaTypeName.APPLICATION_JSON.value: MediaType(
                                        schema=Pet().component_name
                                    )
                                }
                            )
                        }
                    )
                ),
            )
        )
```

And it generates 5 properties for `APISpec.path` core API:
- `path`
- `operations`
- `summary`
- `description`
- `parameters`

> **_NOTE:_** Directly access properties undefined in `PathItem` will cause the `KeyError` exception.

```python
# return "/pet"
GetPetAPI().path

# return
# {
#     "operations": { 
#         "get": {
#             "responses": { 
#                 "200": {
#                     "content": { 
#                         "application/json": {
#                             "schema": "PaginatedSupportedCurrency" 
#                         }
#                     }
#                 }
#             }
#     }
# }
GetPetAPI().operations

# throws KeyError as it's undefined
GetPetAPI().description
GetPetAPI().summary
GetPetAPI().parameters
```

They can be used as parameter with same name for `APISpec.path` core API.

```python
spec.path(
    path=GetPetAPI().path,
    operations=GetPetAPI().operation
)
```

Similarly, `PathBase` has the `apispec_parameter` property to generate parameter dictionary:

```python
spec.path(**GetPetAPI().apispec_parameter)
```

### Pre-Defined Class

As notes the [Basic](#basic) section show, the **apispec-helper** provides Classes with pre-defined value members. You can leverage them when creating OpenAPI Objects. For instance, you can use `comonent.NumberFormat` when specifying `Number` format

```python
Number(
    format_=NumberFormat.FLOAT
)
```

In yaml file, it will be replaced with "float"

```yaml
# ... snipt
type: "number"
format: "float"  
```

### Keyword replacement

Some keywords in OpenAPI Specification conflict with Python keywords. For instance, `in` and `format`. These keywords are with underline(`_`) postfix to prevent conflict(`in_` and `format_`) in **apispec-helper**. When converting these Objects to dictionary, underline in these keywords will be removed. We won't see them in dictionaries and yaml outputs.

### Referencing

The apispec can [generate reference statements](https://apispec.readthedocs.io/en/latest/special_topics.html#referencing-top-level-components), so for fields allow referencing, you can directly provide component names instead of adding `"$ref": "..."` by yourself, which also works in **apispec-helper**. Some Class fields accept `str` type value instead of OpenAPI Object type, which means you can pass component name to apispec to generate references. See the `PaginatedPetPet` example in the [Overview](#overview) section.

## Todo

PRs are welcomed to this project:

1. Unitest to cover all OpenAPI Objects
2. Support all fields and all OpenAPI Objects
3. More thorough API documents
