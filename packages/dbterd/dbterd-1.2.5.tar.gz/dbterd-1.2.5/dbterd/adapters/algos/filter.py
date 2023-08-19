import sys
from fnmatch import fnmatch
from typing import List

from dbterd.adapters.algos.meta import Table


def is_selected_table(
    table: Table,
    select_rules: List[str] = [],
    exclude_rules: List[str] = [],
    resource_types: List[str] = ["model"],
):
    """Check if Table is selected with defined selection criteria

    Args:
        table (Table): Table object
        select_rules (List[str]): Selection rules. Defaults to [].
        exclude_rules (List[str], optional): Exclusion rules. Defaults to [].
        resource_types (List[str], optional): Selected resource types. Defaults to [].

    Returns:
        bool: True if Table is selected. False if Tables is excluded
    """
    # Selection
    selected = True
    if select_rules:
        selected = any([evaluate_rule(table=table, rule=rule) for rule in select_rules])
    if resource_types:
        selected = selected and table.resource_type in resource_types
    # Exclusion
    excluded = False
    if exclude_rules:
        excluded = any(
            [evaluate_rule(table=table, rule=rule) for rule in exclude_rules]
        )

    return selected and not excluded


def evaluate_rule(table: Table, rule: str):
    """Evaluate selection/exclusion single rule with AND logic applied

    Args:
        table (Table): Table object to be evaluated
        rule (str): Rule defintion

    Returns:
        bool: True if satisfied all rules
    """
    and_parts = rule.split(",")
    results = []
    for x in and_parts:
        rule_parts = x.lower().split(":")
        type, rule = "name", rule_parts[0]
        if len(rule_parts) > 1:
            type, rule = tuple(rule_parts[:2])
        selected_func = getattr(sys.modules[__name__], f"__is_satisfied_by_{type}")
        results.append(selected_func(table=table, rule=rule))
    return all(results)


def __is_satisfied_by_name(table: Table, rule: str = ""):
    """Evaulate rule by Name

    Args:
        table (Table): Table object
        rule (str, optional): Rule def. Defaults to "".

    Returns:
        bool: True if satisfied `starts with` logic applied to Table name
    """
    if not rule:
        return True
    return table.name.startswith(rule)


def __is_satisfied_by_schema(table: Table, rule: str = ""):
    """Evaulate rule by Schema name

    Args:
        table (Table): Table object
        rule (str, optional): Rule def. Defaults to "".

    Returns:
        bool: True if satisfied `starts with` logic applied to Table's schema
    """
    if not rule:
        return True

    parts = rule.split(".")
    selected_schema = parts[-1]
    selected_database = parts[0] if len(parts) > 1 else table.database
    return f"{table.database}.{table.schema}".startswith(
        f"{selected_database}.{selected_schema}"
    )


def __is_satisfied_by_wildcard(table: Table, rule: str = "*"):
    """Evaulate rule by Wildcard (Unix Style)

    Args:
        table (Table): Table object
        rule (str, optional): Rule def. Defaults to "".

    Returns:
        bool: True if satisfied table name matched the pattern
    """
    if not rule:
        return True
    return fnmatch(table.name, rule)
