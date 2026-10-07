"""Validate the closed JSON Schema keyword subset shipped here; no dependency.

Unsupported keywords fail closed. This is not a general Draft 2020-12 implementation.
CSV contracts and cross-record semantics are validated separately.
"""
import json
import re
from common import number,as_date,confined

ALLOWED={'$schema','title','description','type','properties','required','additionalProperties',
         'enum','minimum','maximum','minLength','pattern','format','anyOf'}
MAPPING={'source':'08_evidence/source_library.csv','evidence':'08_evidence/evidence_register.csv',
         'opportunity':'05_opportunities/opportunity_database.csv','risk':'06_risks/risk_register.csv',
         'competitor':'03_competitors/competitor_database.csv','customer_segment':'04_customers/customer_segments_template.csv'}

def check_schema(schema):
    if not isinstance(schema,dict) or set(schema)-ALLOWED: raise ValueError('Unsupported or malformed schema keywords')
    typ=schema.get('type')
    if typ is not None and typ not in ('object','string','number','integer','null'): raise ValueError('Unsupported schema type')
    if 'anyOf' in schema:
        if not isinstance(schema['anyOf'],list) or not schema['anyOf']: raise ValueError('Invalid anyOf')
        for child in schema['anyOf']: check_schema(child)
    if typ=='object':
        if not isinstance(schema.get('properties'),dict) or not isinstance(schema.get('required'),list): raise ValueError('Invalid object schema')
        if len(set(schema['required']))!=len(schema['required']) or not set(schema['required'])<=set(schema['properties']): raise ValueError('Invalid required fields')
        if schema.get('additionalProperties') is not False: raise ValueError('Object schema must reject extra properties')
        for child in schema['properties'].values(): check_schema(child)
    for key in ('minimum','maximum','minLength'):
        if key in schema: number(schema[key],-1e20,1e20)
    if 'minimum' in schema and 'maximum' in schema and schema['minimum']>schema['maximum']: raise ValueError('Reversed schema bounds')
    if 'enum' in schema and (not isinstance(schema['enum'],list) or not schema['enum']): raise ValueError('Invalid enum')
    if 'format' in schema and schema['format']!='date': raise ValueError('Unsupported schema format')
    if 'pattern' in schema: re.compile(schema['pattern'])

def errors_for(value,schema,path='$'):
    errors=[]
    if 'anyOf' in schema:
        if not any(not errors_for(value,child,path) for child in schema['anyOf']): errors.append(path+': no allowed optional type matches')
        return errors
    typ=schema.get('type')
    valid={'object':isinstance(value,dict),'string':isinstance(value,str),
           'number':type(value) in (int,float),'integer':type(value) is int,
           'null':value is None}.get(typ,True)
    if not valid: return [path+': invalid type']
    if 'enum' in schema and value not in schema['enum']:errors.append(path+': unsupported enum')
    if typ=='object':
        for field in schema['required']:
            if field not in value:errors.append(path+'.'+field+': missing required property')
        if schema.get('additionalProperties') is False and set(value)-set(schema['properties']):errors.append(path+': unexpected properties')
        for field,child in schema['properties'].items():
            if field in value:errors+=errors_for(value[field],child,path+'.'+field)
    elif typ in ('number','integer'):
        try:number(value,schema.get('minimum',-1e20),schema.get('maximum',1e20))
        except ValueError:errors.append(path+': invalid finite numeric range')
    elif typ=='string':
        if len(value)<schema.get('minLength',0):errors.append(path+': too short')
        if 'pattern' in schema and not re.search(schema['pattern'],value):errors.append(path+': invalid pattern')
        if schema.get('format')=='date':
            try:as_date(value)
            except ValueError:errors.append(path+': invalid ISO date')
    return errors

def to_json(row,contract):
    result={}
    for field,value in row.items():
        if value=='' and field not in contract['required']:result[field]=None
        elif field in contract['ranges']:
            n=number(value,*contract['ranges'][field])
            if field in contract.get('integers',[]):
                if not n.is_integer():raise ValueError('Integer field has fractional value')
                n=int(n)
            result[field]=n
        else:result[field]=value
    return result

def validate_schemas(root,contract,data):
    errors=[]
    for name,path in MAPPING.items():
        try:
            schema=json.loads(confined(root,f'schemas/{name}_schema.json',True).read_text(encoding='utf-8'))
            check_schema(schema)
            if set(schema['properties'])!=set(contract[path]['fields']) or schema['required']!=contract[path]['required']:raise ValueError('Schema/CSV contract mismatch')
            for field in contract[path]['ranges']:
                prop=schema['properties'][field]
                if 'anyOf' in prop:prop=prop['anyOf'][0]
                if [prop.get('minimum'),prop.get('maximum')]!=contract[path]['ranges'][field]:raise ValueError('Range mismatch')
                if prop.get('type')!=('integer' if field in contract[path].get('integers',[]) else 'number'):raise ValueError('Type mismatch')
            for field,enum in contract[path]['enums'].items():
                prop=schema['properties'][field]
                if 'anyOf' in prop:prop=prop['anyOf'][0]
                if prop.get('enum')!=enum:raise ValueError('Enum mismatch')
            for row in data.get(path,[]):
                try:errors+=[name+' schema '+e for e in errors_for(to_json(row,contract[path]),schema)]
                except ValueError:errors.append(name+' schema: CSV conversion rejected')
        except (ValueError,OSError,KeyError,TypeError,re.error):errors.append(name+' schema: invalid or incompatible schema')
    return errors
