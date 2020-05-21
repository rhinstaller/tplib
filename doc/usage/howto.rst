.. _howto:

=====
HOWTO
=====

General
=======

I want to track RHEL-7 and RHEL-8 testcases/requirements separately
-------------------------------------------------------------------
Use separate branches for RHEL-7 and RHEL-8. For each branch that's desired to
be imported to Polarion, specify the branches in ``POLARION_PUSH_BRANCHES``
variable in your deployment. For more info see :ref:`deployment`.

When the branches are used, they will be taken in account during the import to
Polarion. Note that testcases/requirements present in different branches are
considered as different from the point of importer and one should not override
other one (unless explicitly specified by Polarion ID through special field).

Testcases
=========

I want to add a new testcase
----------------------------
 #. Create a new file with ``.tc.yaml`` suffix anywhere you find suitable in
    the repository with testcases.
 #. Fill in the file with information about the testcase in format according to :ref:`testcase_structure`.
 #. Check content of the testcase using :ref:`query.py <tool_query>`.
 #. Commit and push changes.

I want to delete a testcase
---------------------------
 #. Find the testcase file e.g. using :ref:`query.py <tool_query>`: ``query.py -t path/to/testcases 'tc.name == "Name of testcase"' 'tc.filename'``.
 #. Delete the file.
 #. Commit and push changes.

.. note:: Deleted testcases are still available in Polarion and are in inactive
          state.

Requirements
============

I want to add a new requirement with specific testcases
-------------------------------------------------------
Follow instructions the same way as when adding testcase, but use
``.req.yaml`` suffix and follow requirement structure:
:ref:`requirement_structure`.

I want to add link more testcases to requirement
------------------------------------------------
 #. Locate the desired testcases and requirement e.g. by using
    :ref:`query.py <tool_query>`.
 #. Look for ``verified_by`` field and modify its content.

   #. When ``direct-list`` is used, add name of the testcase to the list.
   #. When ``query`` is used, modify the query so that the desired testcases
      match the query. You can use :ref:`query.py <tool_query>` to see effect
      of the changed query: ``query.py -r path/to/testcases 'req.name == "My requirement"' 'req.verificationTestCases'``

 #. Commit and push changes.

I want to delete a requirement
------------------------------
The same applies here as when deleting testcases.

.. note:: Deleted requirements are still available in Polarion and are in
          inactive state.

.. note:: The inactive requirement in Polarion loses all references to
          testcases as it cannot be tracked anymore.

Testplans
=========

TBD

Misc
====

I want to find some specific testcases/requirements
---------------------------------------------------
Use :ref:`query.py <tool_query>` to look for desired testcases/requirements.
To find information about testcase properties, see :py:class:`testcases.structures.testcase.TestCase` or :py:class:`testcases.structures.requirement.Requirement` respectively.

Example: ``query.py -t path/to/testcases '"Hello" in tc.tags' 'tc.filename'``.
