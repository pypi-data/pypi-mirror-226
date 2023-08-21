import os
import sys
from types import SimpleNamespace

from . import utils

logger = utils.init_logger('go.provision')


class Helper:
    def __init__(self, working_directory, workspace, verbose, dry_run):
        self.working_directory = working_directory
        self.workspace = workspace
        self.verbose = verbose
        self.dry_run = dry_run

    def initialize(self):
        cmd = "terraform -chdir={} init -reconfigure".format(self.working_directory)
        if not self.dry_run:
            print(cmd)
            import os

            os.system(cmd)
        else:
            logger.info(cmd)

    def select_workspace(self):
        assert self.workspace
        result = self.get_current_workspace()

        if result != self.workspace:
            workspaces = self.list_workspaces()

            if not self.dry_run:
                if self.workspace not in workspaces:
                    raise Exception(f'Workspace {self.workspace} does not exist.')

                cmd = "terraform -chdir={} workspace select {}".format(self.working_directory, self.workspace)
                utils.execute(cmd)

    def select_or_create_workspace(self):
        assert self.workspace
        result = self.get_current_workspace()

        if result != self.workspace:
            workspaces = self.list_workspaces()

            if not self.dry_run:
                if self.workspace not in workspaces:
                    cmd = "terraform -chdir={} workspace new {}".format(self.working_directory, self.workspace)
                else:
                    cmd = "terraform -chdir={} workspace select {}".format(self.working_directory, self.workspace)

                utils.execute(cmd)

    def delete_workspace(self):
        assert self.workspace
        if not self.dry_run:
            workspaces = self.list_workspaces()

            if self.workspace not in workspaces:
                raise Exception(f'Workspace {self.workspace} does not exist.')

            result = self.get_current_workspace()

            assert result == self.workspace
            cmd = "terraform -chdir={} workspace select default".format(self.working_directory)
            utils.execute(cmd)
            cmd = "terraform -chdir={} workspace delete {}".format(self.working_directory, self.workspace)
            utils.execute(cmd)
        else:
            cmd = "terraform -chdir={} workspace select default".format(self.working_directory)
            logger.info(cmd)
            cmd = "terraform -chdir={} workspace delete {}".format(self.working_directory, self.workspace)
            logger.info(cmd)

    def list_workspaces(self):
        cmd = "terraform -chdir={} workspace list".format(self.working_directory)

        if self.dry_run:
            logger.info(cmd)
            return []

        result = utils.execute(cmd)
        return result.split()

    def get_current_workspace(self):
        cmd = "terraform -chdir={} workspace show".format(self.working_directory)

        if self.dry_run:
            logger.info(cmd)
            return None

        result = utils.execute(cmd)
        return result.strip()

    def apply(self, var_file):
        cmd = "terraform -chdir={} apply -auto-approve -var-file={}".format(self.working_directory, var_file)

        if self.dry_run:
            logger.info(cmd)
            return

        result = utils.execute(cmd)

        if self.verbose:
            logger.info(result)

    def show(self):
        cmd = "terraform -chdir={} show".format(self.working_directory)

        if self.dry_run:
            logger.info(cmd)
            return

        result = utils.execute(cmd)
        print(result)

    def output(self):
        cmd = "terraform -chdir={} output".format(self.working_directory)

        if self.dry_run:
            logger.info(cmd)
            return

        result = utils.execute(cmd)
        print(result)

    def destroy(self):
        cmd = "terraform -chdir={} destroy -auto-approve".format(self.working_directory)

        if self.dry_run:
            logger.info(cmd)
            return

        result = utils.execute(cmd)

        if self.verbose:
            logger.info(result)

    def get_public_ip(self):
        cmd = 'terraform -chdir={} output -raw public_ip'.format(self.working_directory)

        if self.dry_run:
            logger.info(cmd)
            return "xxx.xxx.xxx.xxx"

        result = utils.execute(cmd)
        return result.strip()

    def play_book(self, inventory_file, script, ansible_vars):
        cmd = ['ansible-playbook']

        for k, v in ansible_vars.items():
            cmd.append('-e')
            cmd.append('{}="{}"'.format(k, v))

        cmd.append('-i')
        cmd.append(inventory_file)
        cmd.append(script)

        if self.dry_run:
            logger.info(' '.join(cmd))
            return

        result = utils.execute(cmd)

        if self.verbose:
            logger.info(script + result)


# noinspection PyArgumentList
def main(argv=None):
    argv = argv or sys.argv[1:]
    parser = utils.build_parser()
    args = parser.parse_args(argv)

    if not os.path.isdir(args.working_directory):
        logger.error(f'{args.working_directory} is not a directory')
        sys.exit(1)

    if args.workspace and args.workspace == 'default':
        logger.error('workspace cannot be default')
        sys.exit(1)

    helper = Helper(args.working_directory, args.workspace, args.verbose, args.dry_run)

    if args.init:
        helper.initialize()
        return

    if args.list_workspaces:
        workspaces = helper.list_workspaces()

        if not args.dry_run:
            workspaces.remove('*')
            print(workspaces)
        return

    if not args.workspace:
        logger.error('must specify a workspace')
        sys.exit(1)

    if args.destroy:
        helper.select_workspace()
        helper.destroy()
        helper.delete_workspace()
        return

    if args.show:
        helper.select_workspace()
        helper.show()
        return

    if args.output:
        helper.select_workspace()
        helper.output()
        return

    if not args.conf:
        return

    helper.select_or_create_workspace()
    config = utils.read_config(args.conf)
    config = SimpleNamespace(**config)
    config.ssh_keys = SimpleNamespace(**config.ssh_keys)

    from .ssh_helper import parse_private_key, parse_public_key

    if not os.path.isfile(config.ssh_keys.private):
        logger.error(f'unable to read private key at {config.ssh_keys.private}')
        sys.exit(1)

    parse_private_key(config.ssh_keys.private)

    if not os.path.isfile(config.ssh_keys.public):
        logger.error(f'unable to read public key at {config.ssh_keys.public}')
        sys.exit(1)

    parse_public_key(config.ssh_keys.public)

    have_runtime = hasattr(config, "runtime")

    if have_runtime:
        config.runtime = SimpleNamespace(**config.runtime)
    else:
        config.runtime = SimpleNamespace()

    if not hasattr(config.runtime, "ssh_user"):
        config.runtime.ssh_user = 'ubuntu'

    if not hasattr(config.runtime, "ssh_port"):
        config.runtime.ssh_port = 22

    have_instance = hasattr(config, "instance")

    if have_instance:
        config.instance = SimpleNamespace(**config.instance)
    else:
        config.instance = SimpleNamespace()

    have_stack = hasattr(config, "stack")

    if have_stack:
        config.stack = SimpleNamespace(**config.stack)
    else:
        config.stack = SimpleNamespace()

    if not utils.check_ssh_keys(config.ssh_keys):
        logger.error('check ssh keys:may not exist')
        sys.exit(1)

    config.instance.public_key_path = config.ssh_keys.public

    if not args.dry_run:
        workspace = helper.get_current_workspace()
        logger.info("using workspace=" + workspace)

    if have_instance:
        config.instance.tags['Workspace'] = args.workspace
        var_file = os.path.abspath(args.workspace + '.tfvars.json')

        if not args.dry_run:
            utils.write_ns_to_json_file(config.instance, var_file)
        elif args.verbose:
            logger.info("var file contents:" + str(config.instance))

        helper.apply(var_file)

    public_ip = helper.get_public_ip()

    if not args.dry_run:
        logger.info(f'Public ip is {public_ip}')
        username = config.runtime.ssh_user
        port = config.runtime.ssh_port
        key = config.ssh_keys.private
        utils.test_ssh_connection_using_paramiko(public_ip, username, key, port)

    inventory_file = os.path.abspath(args.workspace + '-inventory.cfg')
    host_string = utils.inventory_string(public_ip,
                                         config.runtime.ssh_user,
                                         config.runtime.ssh_port,
                                         config.ssh_keys.private)

    if not args.dry_run:
        if args.verbose:
            logger.info(f"creating ansible inventory file {inventory_file}: {host_string}")

        utils.write_inventory_file(inventory_file, host_string)
    else:
        if args.verbose:
            logger.info(f"entry in ansible inventory file would look like: {host_string}")

    if have_stack:
        for script in config.stack.scripts:
            helper.play_book(inventory_file, script, config.stack.vars)


if __name__ == "__main__":
    main(sys.argv[1:])
