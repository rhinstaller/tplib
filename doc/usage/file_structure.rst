.. _file_structure:

==============
File structure
==============

There's no filesystem organization structure where test plans, requirements and
test cases are discovered by :py:class:`testcases.library.Library`. All the
structures should be then accessed through the
:py:class:`testcases.library.Library` object.

Structures are destinguished by their filename suffix (described below) and
are available in :py:class:`testcases.library.Library` after successful load.
If a file doesn't contain correct structure, there will be error raised during
discovery.

.. _testplan_structure:

Test plan
=========

:suffix: ``.plan.yaml``
:class: :py:class:`tclib.structures.testplan.TestPlan`
:library attribute: ``testplans``
:yaml structure:

  * **name** (`str`, `unique`) -- Test plan name. Used as identifier that can
    be used in **parent_plan** field of other test plans.
  * **description** (`str`, `optional`) -- Description of the testplan
    providing information about the purpose of the test plan, possibly
    specifying who the stakeholders are, turnaround times and other possibly
    useful information.
  * **point_person** (`str`, `inherited`) -- Identifier of person responsible
    for maintenance of this test plan.
  * **tags** (`set`, `inherited`, `optional`) -- Set of strings that can be used
    for categorization purposes.
  * **artifact_type** (`str`, `inherited`) -- Artifact which is handled by the
    test plan. This can be any string. The idea is to use dots as separators
    allowing fine grained specification for which artifacts and under which
    circumstances should this test plan be started. For example, there could
    be an artifact called `package` which can be e.g. `built`, `deleted` or
    `accepted` and the package itself could be e.g. `production` or `scratch`.
    If one would like to have the test plan executed for anything that
    happens with the package, then artifact_type would be just plain
    `package`. If one would like to execute the test plan only for scratch
    packages at the moment they were built, then artifact_type would be
    `package.built.scratch`. Please consult with the execution tooling
    (pipeline) that uses tclib for storing test plans data.
  * **components** (`set`, `inherited`, `optional`) -- Set of component names related to the testplan
  * **execute_on** (`list`, `inherited`) -- Define additional conditions for
    the test plan execution.

    * **type** (`str`) --
    * **filter** (`str`) -- Jinja2 expression, for more information consult
      with the execution tooling (pipeline) that uses tclib for storing test
      plans data.

  * **parent_plan** (`str`, `optional`) -- **name** of other plan which should
    be used as parent for this plan allowing inheritance of certain fields.
    Circular inheritance (A -> B -> A -> ...) is not allowed and will result
    in error as well as referencing non-existing test plan.
  * **verified_by** (`dict` - :py:class:`tclib.structures.testplan.Selection`, `optional`)

    * **test_cases** (`dict` - :py:class:`tclib.structures.testplan.QueryObject`, `optional`)

      * **direct_list** (`list`) -- List of testcase names
      * **query** (`str`) -- Jinja2 expression, see more here: TBD
      * **named_query** (`str`) -- Reference to query, not implemented

    * **requirements** (`dict` - :py:class:`tclib.structures.testplan.QueryObject`, `optional`)

      * **direct_list** (`list`) -- List of requirement names
      * **query** (`str`) -- Jinja2 expression, see more here: TBD
      * **named_query** (`str`) -- Reference to query, not implemented

  * **acceptance_criteria** (`dict` - :py:class:`tclib.structures.testplan.Selection`, `optional`) -- Same as **verified_by**
  * **reporting** (`list`, `inherited`)

    * **type** (`str`) -- Name of reporting should be used while executing the test plan.
    * **condition** (`str`) -- Jinja2 expression used to determine when this reporting definition should be used. One may limit using the reporting only in cases of some events.
    * **group_by** (`list`) -- List of testcases configuration keys based on which the reporting should be grouped.
    * **data** -- Data consumed by automation for purposes of reporting done by the used reporting type. There's no type restriction for this structure.

  * **configurations** (`list`, `inherited`, `optional`) --
  * **document** (`str`, `optional`) --

.. _requirement_structure:

Examples
--------

.. literalinclude:: ../../examples/testplans/testplan-main-1.plan.yaml
   :language: yaml

.. literalinclude:: ../../examples/testplans/testplan-sub-1.plan.yaml
   :language: yaml

Requirement
===========

:suffix: ``.req.yaml``
:class: :py:class:`tclib.structures.requirement.Requirement`
:library attribute: ``requirements``
:yaml structure:

  * **name** (`str`, `unique`) --
  * **description** (`str`, `optional`) --
  * **tags** (`list`) --
  * **verified_by** (`dict` - :py:class:`tclib.structures.requirement.QueryObject`, `optional`)

    * **direct_list** (`list`) -- List of testcase names
    * **query** (`str`) -- Jinja2 expression, see more here: TBD
    * **named_query** (`str`) -- Reference to query, not implemented

  * **acceptance_criteria** (`dict` - :py:class:`tclib.structures.requirement.QueryObject`, `optional`) -- Same as **verified_by**

Examples
--------

.. literalinclude:: ../../examples/requirements/requirement-first.req.yaml
   :language: yaml

.. literalinclude:: ../../examples/requirements/requirement-priority.req.yaml
   :language: yaml

.. _testcase_structure:

Test case
=========
:suffix: ``.tc.yaml``
:class: :py:class:`tclib.structures.testcase.TestCase`
:library attribute: ``testcases``
:yaml structure:

 * **name** (`str`, `unique`) -- Test case name used as identifier inside
   library
 * **description** (`str`) -- TODO
 * **priority** (`int`) -- This can be theoretically any number. Convention
   is to use values in range <1,10> where higher number means higher priority.
 * **components** (`list`, `optional`) -- List of components covered by the
   test case.
 * **execution** (`dict`) --

   * **type** (`str`) -- This field is used by automation of testcase
     execution (pipeline) where the value signals what kind of execution is
     used for this test case. Special word `manual` is used to signal that
     manual (human) execution is required and no automation is available.
     The `manual` word is also interpreted when the testcase is exported e.g.
     to Polarion.
   * **automation_data** (any type, optional) -- The data type depends on the
     automation of testcase execution (pipeline) and can be used as
     machine-readable execution instructions. This field can be used even
     in case of `manual` for purposes of some upcoming automation.

 * **filter** (`list`, `optional`) -- TBD
 * **instructions** (`dict` - :py:class:`tclib.structures.testcase.Instructions`)

   * **setup** (`list`, `optional`) -- list of :py:class:`tclib.structures.testcase.Instruction`

     :variable item (full):
      * **step** (`str`) --
      * **result** (`str`, `optional`) -- (default: 'Success')

     :variable item (short):
        * `str` -- Used as **step** with default **result**
   * **steps** (`list`) -- same as **setup**
   * **teardown** (`list`, `optional`) -- same as **setup**

 * **configurations** (`list`, `optional`) -- 
 * **author**: (`str`, `optional`) -- Name of test case author
 * **tags**: (`list`, `optional`) -- List of strings used as tags for queries.

Examples
--------

.. literalinclude:: ../../examples/testcases/testcase-manual-1.tc.yaml
   :language: yaml

.. literalinclude:: ../../examples/testcases/testcase-automated-1.tc.yaml
   :language: yaml

.. literalinclude:: ../../examples/testcases/testcase-disabled-1.tc.yaml
   :language: yaml
